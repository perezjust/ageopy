import arcpy
import os, string, sys, traceback
from os.path import join


import gpFuncs as gpF
from gpFuncs import *
import expFuncs as expF
from expFuncs import *

'''
    TODO:

'''


def main():



    try:

        #Parameters
        parcel = arcpy.GetParameterAsText(0)
        tractnumberfield = arcpy.GetParameterAsText(1)
        route = arcpy.GetParameterAsText(2)
        easement = arcpy.GetParameterAsText(3)
        rowtype = arcpy.GetParameterAsText(4)
        wkspace = arcpy.GetParameterAsText(5)

        #Geoprocessing with route feature class needs result in non-routed feature classes
        arcpy.env.outputMFlag = "Disabled"

        #Step 1 - Intersect parcels and easements
        parcelXEaseDissFL = parcelIntersectEasement(parcel, easement, route, wkspace, rowtype, tractnumberfield)

        #Step 2 - Add approximate station value to Easements intersected table for those easements that do not intersect the centerline and would not get a measure value later on!!!!
        locateCentroidOfEasement(parcelXEaseDissFL, route, wkspace, rowtype, tractnumberfield)

        #Step 3 - Pivot the easements intersection table
        pivotTable_Dict = buildPivotTable_Dict(parcelXEaseDissFL, wkspace, rowtype, tractnumberfield)

        #Step 4 - Intersect parcels and centerline
        clSegmentsFL = parcelIntersectCenterline(parcel, route, wkspace)

        #Step 5 - Find centerline segments that have the same parcel number (duplicates or overlaps) and then for each find those that cross more than one parcel due to parcel overlap
        multipleCrossings_Dict = findMultipleCrossings(clSegmentsFL, parcel, tractnumberfield)

        #Step 6 - Locate the centerline segments on the route... result table will be the final Parcel Impact table
        locateFeatures = buildLocateFeaturesTable(clSegmentsFL, route, wkspace)

        #Step 7 - Using the multipleCrossings_Dict dictionary, set the values of those cl segments which have been identified as duplicate/overlap respectively and then build a list of these segments to ignore when updating table with easement acreages
        finishTable_List = calculateDuplicateRows(locateFeatures, multipleCrossings_Dict, tractnumberfield)

        #Step 8 - Insert into the table those easement pivoted values while ignoring those segments contained in the finishTable_List
        finishTable(locateFeatures, pivotTable_Dict, finishTable_List, tractnumberfield)

        arcpy.SetParameter(6, clSegmentsFL.path)
        arcpy.SetParameter(7, locateFeatures)
        arcpy.SetParameter(8, parcelXEaseDissFL.path)

    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()







def parcelIntersectEasement(parcel, easement, route, wkspace, rowTypeField, tractNumField):
    fl = gpF.featureLayer(parcel)
    parcelXEase = fl.intersect(easement)
    parcelXEaseDiss = arcpy.CreateUniqueName("parcelXEaseDiss.shp", wkspace)
    arcpy.Dissolve_management(parcelXEase, parcelXEaseDiss, [rowTypeField, tractNumField])
    parcelXEaseDissFL = gpF.featureLayer(parcelXEaseDiss)
    arcpy.AddField_management(parcelXEaseDissFL.path, "Acreage", "Double", "", "")
    arcpy.CalculateField_management(parcelXEaseDissFL.path, "Acreage", "!shape.area@acre!", "PYTHON")
    #findApproximateStationOfEasement(parcelXEaseDissFL, route, wkspace)
    return parcelXEaseDissFL



def parcelIntersectCenterline(parcel, centerline, wkspace):
    fl = gpF.featureLayer(parcel)
    parcelXCL = gpF.featureLayer(fl.intersect(centerline))
    clSegments = arcpy.CreateUniqueName("clSegments.shp", wkspace)
    '''
        Use the exploded features to check for overlap
    '''
    arcpy.MultipartToSinglepart_management(parcelXCL.path, clSegments)
    clSegmentsFL = gpF.featureLayer(clSegments)
    clSegmentsFL.addGUIDField()
    arcpy.AddField_management(clSegmentsFL.path, "CL_X_Feet", "Text",  "", "")
    arcpy.CalculateField_management(clSegmentsFL.path, "CL_X_Feet", "!shape.length@feet!", "PYTHON")
    return clSegmentsFL



def buildLocateFeaturesTable(featLayerObject, route, wkspace):
    '''
        I want to create a table that will have all the intersected segments of the centerline & parcels.
        I want this table to be passed to a function which should fill out the acreages using a
        pivot table function.
    '''
    locateFeatures = arcpy.CreateUniqueName("Parcel_Impact_Table.dbf", wkspace)
    arcpy.LocateFeaturesAlongRoutes_lr(featLayerObject.path, route, "CL_NAME", "1 Feet", locateFeatures, "RID LINE FMEAS TMEAS")
    addFields_Dict = {'FromMP' : 'Text', 'ToMP' : 'Text', 'ApproxMP' : 'Text', 'PermX_Acre' : 'Text', 'TempX_Acre' : 'Text', 'ATWSX_Acre' : 'Text', 'ROWImpact' : 'Text'}
    for aFD in addFields_Dict:
        arcpy.AddField_management(locateFeatures, aFD, addFields_Dict[aFD], "", "")
    ucur = arcpy.UpdateCursor(locateFeatures)
    for urow in ucur:
        urow.ROWImpact = "CENTERLINE"
        urow.ToMP = "%.1f" %float(urow.TMEAS / 5280)
        urow.FromMP = "%.1f" %float(urow.FMEAS / 5280)
        urow.ApproxMP = calcMidDistance("%.1f" %float(urow.TMEAS / 5280), "%.1f" %float(urow.FMEAS / 5280))
        ucur.updateRow(urow)
    return locateFeatures



def buildPivotTable_Dict(featureLayerObject, wkspace, rowTypeField, tractNumField):
    pivotTable_Dict = {}
    for item in featureLayerObject.makeQueryListUnique(tractNumField):
        sql = '"' + tractNumField + '"' + " = " + "'" + item + "'"
        scur = arcpy.SearchCursor(featureLayerObject.path, sql)
        atws = ""
        temp = ""
        perm = ""
        apprx = ""
        row_type = ""
        for srow in scur:
            row_type = srow.getValue(rowTypeField)
            if row_type == "ATWS":
                atws = srow.getValue("Acreage")
            elif row_type == "TEMPORARY EASEMENT":
                temp = srow.getValue("Acreage")
            elif row_type == "PERMANENT EASEMENT":
                perm = srow.getValue("Acreage")
            elif row_type == "ApproxSta":
                apprx = srow.getValue("Acreage")
            else:
                pass
        pivotTable_Dict[item] = str(atws) + "@!@" + str(temp) + "@!@" + str(perm) + "@!@" + str(apprx)

    return pivotTable_Dict



def locateCentroidOfEasement(featureLayerObject, route, wkspace, rowTypeField, tractNumField):
    locateFeatures = arcpy.CreateUniqueName("Centroid_Easements_ApproxStat.dbf", wkspace)
    approxStationFeatures = arcpy.CreateUniqueName("approxStationFeatures.shp", wkspace)
    arcpy.Dissolve_management(featureLayerObject.path, approxStationFeatures, tractNumField)
    approxStationFeaturesPoints = arcpy.CreateUniqueName("approxStationFeaturesPoints.shp", wkspace)
    arcpy.CreateFeatureclass_management(os.path.dirname(approxStationFeaturesPoints), os.path.basename(approxStationFeaturesPoints),"POINT", "", "", "", featureLayerObject.path[:-4] + ".prj")
    arcpy.AddField_management(approxStationFeaturesPoints, tractNumField, "Text")
    arcpy.AddField_management(approxStationFeaturesPoints, "XCoord", "Text")
    arcpy.AddField_management(approxStationFeaturesPoints, "YCoord", "Text")
    icur = arcpy.InsertCursor(approxStationFeaturesPoints)
    scur = arcpy.SearchCursor(approxStationFeatures)
    for srow in scur:
        '''

        !!!!!!!!<----L-O-O-K--H-E-R-E---->Here you can add new fields to final table

        '''
        pnt = arcpy.Point(srow.shape.centroid.X, srow.shape.centroid.Y)
        feat = icur.newRow()
        feat.shape = pnt
        feat.setValue(tractNumField, srow.getValue(tractNumField))
        feat.setValue("XCoord", srow.shape.centroid.X)
        feat.setValue("YCoord", srow.shape.centroid.Y)
        icur.insertRow(feat)
    #arcpy.AddXY_management(approxStationFeaturesPoints)
    arcpy.LocateFeaturesAlongRoutes_lr(approxStationFeaturesPoints, route, "CL_NAME", "100 miles", locateFeatures, "RID POINT MEAS")
    del srow, scur, icur, feat
    approxStatDict = {}
    scur = arcpy.SearchCursor(locateFeatures)
    for srow in scur:
        approxStatDict[srow.getValue(tractNumField)] = "%.1f" %float(srow.MEAS / 5280)
    del srow, scur
    icur = arcpy.InsertCursor(featureLayerObject.path)
    for tract in approxStatDict:
        irow = icur.newRow()
        irow.setValue(tractNumField, tract)
        irow.setValue(rowTypeField, "ApproxSta")
        irow.Acreage = approxStatDict[tract]
        icur.insertRow(irow)
    del icur, irow



def calculateDuplicateRows(table, inDict, tractNumField):
    '''
        Example dictionary.. over=overlap set, dup=duplicate set, a=overlap feature, b=non-overlap feature
        If a tract has overlap or duplicates the item of the dictionary will have either "over" or "dup".  The features
        that causes the overlap or duplicate were tagged with an "a" or "b" so that we can update each record in the Impact
        Table precisely.

        {
          u'over@!@HL-TX-HS-00022.000': [u'b@!@{c51a28d8-efd7-4342-9ec6-06f39fb65d68}', u'a@!@{cfe99173-e833-412b-9c94-8668187994ee}'],
          u'over@!@HL-TX-LB-00155.000': [u'b@!@{41720615-7156-4b55-b82d-51f36e2866f8}', u'a@!@{768b7153-75e1-41ea-bb55-454e2a922816}'],
          u'dup@!@HL-TX-LB-00191.000': [u'b@!@{75266263-17d8-4928-940a-5d06a930377d}', u'b@!@{1a5ea3fa-fb66-4881-af34-062ceae4f1a5}'],
          u'over@!@HL-TX-LB-00146.000': [u'b@!@{e680a83a-8020-4ec0-a5e7-8e45f510f3a0}', u'a@!@{4fbae28a-ad6a-4f4e-bd5c-1445c60a213a}'],
          u'over@!@HL-TX-HS-00021.000': [u'b@!@{fc2316c4-2809-4e9a-bbe8-eb58521eb39f}', u'a@!@{5609b2ee-6cf4-4da8-86c3-bfbfbeabb9c2}']
        }
    '''

    sqlPivotTableList = []

    for item_uniqueTRACTNUM in inDict:
        itemsplit = item_uniqueTRACTNUM.split("@!@")

        #Overlap
        if itemsplit[0] == "over":
            guidList = inDict[item_uniqueTRACTNUM]
            for guidVal in guidList:
                guidsplit = guidVal.split("@!@")
                if guidsplit[0] == "a":
                    sql = '"' + tractNumField + '"' + " = " + "'" + itemsplit[1] + "'" + ' AND ' + '"' + 'GUID_O' + '"' + " = " + "'" + guidsplit[1] + "'"
                    ucur = arcpy.UpdateCursor(table, sql)
                    for urow in ucur:
                        urow.PermX_Acre = "OVERLAP"
                        urow.TempX_Acre = "OVERLAP"
                        urow.ATWSX_Acre = "OVERLAP"
                        ucur.updateRow(urow)
                        sqlPivotTableList.append(guidsplit[1])
                    del ucur, urow

        #Duplicate
        else:
            find1stRecordCounter = 0
            sql = '"' + tractNumField + '"' + " = " + "'" + itemsplit[1] + "'"

            arcpy.AddMessage(sql)
            ucur = arcpy.UpdateCursor(table, sql, "", "", "FMEAS")
            for urow in ucur:
                find1stRecordCounter  += 1
                if find1stRecordCounter > 1:
                    sqlPivotTableList.append(urow.getValue("GUID_O"))
                    urow.PermX_Acre = "DUPLICATE"
                    urow.TempX_Acre = "DUPLICATE"
                    urow.ATWSX_Acre = "DUPLICATE"
                    ucur.updateRow(urow)
                else:
                    pass
            del ucur, urow

    return sqlPivotTableList



def findMultipleCrossings(featureLayerObject, parcel, tractNumField):
    '''
        **Build a dictionary that has the TRACTNUM values as key and a list of the GUID_O values as
          the item.  If ther TRACTNUM has overlaps then return only the GUID_O values that are overlaps.
          If the TRACTNUM has duplicates then return all the GUID_O values.

        I want to find those features that are duplicated from an intersect wherein a centerline hit
        a polygon in disjoint segments.  These may be proper disjoint segments or via the intersection
        and overlapping polygons the segments would over represent the length across the polygons...in
        this situation I want to calculate those values to say "Overlap"
    '''
    tractnumDict = {}
    arcpy.MakeFeatureLayer_management(parcel, "parcel")
    xingCounter = 0
    rowCounter = 0
    for uniqueTRACTNUM in expF.findDuplicateValue(featureLayerObject.path, tractNumField):
        sql = '"' + tractNumField + '"' + " = " + "'" + uniqueTRACTNUM + "'"
        #Here I have possibly mulitple records returned
        scur = arcpy.SearchCursor(featureLayerObject.path, sql)
        tractnumGUIDList = []
        for srow in scur:
            rowCounter +=1
            feat = srow.shape
            arcpy.SelectLayerByLocation_management("parcel", "CONTAINS", feat, "", "NEW_SELECTION")
            xings = int(arcpy.GetCount_management("parcel").getOutput(0))
            xingCounter += xings
            if xings > 1:
                guidValue = "a@!@" + srow.getValue("GUID_O")
                tractnumGUIDList.append(guidValue)
            else:
                guidValue = "b@!@" + srow.getValue("GUID_O")
                tractnumGUIDList.append(guidValue)
        '''

            Finding whether there is an overlap or duplicate in this set

        '''
        if xingCounter > rowCounter:
            uniqueTRACTNUM1 = "over@!@" + uniqueTRACTNUM
        else:
            uniqueTRACTNUM1 = "dup@!@" + uniqueTRACTNUM

        tractnumDict[uniqueTRACTNUM1] = tractnumGUIDList

    return tractnumDict



def finishTable(table, easementXPivot_Dict, duplicatesToIgnore_List, tractNumField):
    '''

        The easementXPivot_Dict should be a dictionary of the easements intersection results pivoted.
        The duplicatesToIgnore_List came from finding those features that are duplicate or
        are related to overlapping polygon parcels.

        easementXPivot_Dict[item] = str(atws) + "@!@" + str(temp) + "@!@" + str(perm) + "@!@" + str(apprx)

    '''

    scur = arcpy.UpdateCursor(table)
    for srow in scur:
        if srow.getValue("GUID_O") not in duplicatesToIgnore_List:
            tractnum = srow.getValue(tractNumField)
            acreagesSplit = easementXPivot_Dict[tractnum].split("@!@")
            if acreagesSplit[0] == "":
                srow.ATWSX_Acre = 0
            else:
                srow.ATWSX_Acre = acreagesSplit[0]
            if acreagesSplit[1] == "":
                srow.TempX_Acre = 0
            else:
                srow.TempX_Acre = acreagesSplit[1]
            if acreagesSplit[2] == "":
                srow.PermX_Acre = 0
            else:
                srow.PermX_Acre = acreagesSplit[2]
            scur.updateRow(srow)
    del srow, scur

    icur = arcpy.InsertCursor(table)
    for i in easementXPivot_Dict:
        if i not in expF.makeQueryListUnique(table, tractNumField):
            acreagesSplit = easementXPivot_Dict[i].split("@!@")
            irow = icur.newRow()
            irow.setValue(tractNumField, i)
            if acreagesSplit[0] == "":
                irow.ATWSX_Acre = 0
            else:
                irow.ATWSX_Acre = acreagesSplit[0]
            if acreagesSplit[1] == "":
                irow.TempX_Acre = 0
            else:
                irow.TempX_Acre = acreagesSplit[1]
            if acreagesSplit[2] == "":
                irow.PermX_Acre = 0
            else:
                irow.PermX_Acre = acreagesSplit[2]

            irow.ApproxMP = acreagesSplit[3]
            irow.ROWImpact = "EASEMENT"
            icur.insertRow(irow)
    del irow, icur



def calcMidDistance(fmeas, tmeas):
    ameas = float(tmeas) - ((float(tmeas) - float(fmeas))/2)
    return ameas


if __name__ == "__main__":
    main()


