import os, string, sys, traceback, shutil, logging
import arcpy



import expFuncs as eF
from expFuncs import *
import gpFuncs as gpF
from gpFuncs import *


fc = arcpy.GetParameterAsText(0)



exp = meiSetUp("calculateMeasures")
#log = logIt(exp.log_path)
#wkspace = exp.wkspacePath
wkspace = "in_memory"

def main():


    try:
        #Logging
##        log.logTrace("##################################################################################################################")
##        log.logTrace("CalculateMeasures.py ran.")
##        log.logTrace("##################################################################################################################")

        buildFields(fc)
        iterateFeatures(fc)

##        for fc in shapes_List:
##            print "here", fc
##            buildFields(fc)
##            iterateFeatures(fc)

    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()
        #Logging
        #log.logTrace(traceback.format_exc())






def calcLatLong(fc):
    desc = arcpy.Describe(fc)
    if desc.shapeType == "Point":
        if eF.checkForField(fc, "LATITUDE") == 0:
            arcpy.AddField_management(fc, "LATITUDE", "DOUBLE", "", "")
        if eF.checkForField(fc, "LONGITUDE") == 0:
            arcpy.AddField_management(fc, "LONGITUDE", "DOUBLE", "", "")
        #arcpy.CalculateField_management(fc, "LONGITUDE",


def iterateFeatures(fc):
    desc = arcpy.Describe(fc)
    if desc.hasOID == 1:
        oidField = desc.OIDFieldName
        ucur = arcpy.UpdateCursor(fc)
        for urow in ucur:
            objId = str(urow.getValue(oidField))
            arcpy.AddMessage(objId)
            sql = '"' + oidField + '"' + " = " + objId
            mList = getFeatureMeasureValue(fc, sql)
            #print mList
            #if len(mList) > 0:
            if mList is not None:
                try:
                    if desc.shapeType == "Point":

##                        if str(urow.Meas) != str(float(mList[0])):
##                            message = "Meas: ", str(urow.Meas), str(float(mList[0]))
##                            arcpy.AddMessage(message)
                        urow.MEAS = float(mList[0])
                    elif desc.shapeType == "Polyline":

##                        if str(urow.FMeas) != str(float(mList[0])):
##                            message = "FMEAS: ", str(urow.FMeas), str(float(mList[0]))
##                            arcpy.AddMessage(message)
                        urow.FMEAS = float(mList[0])
                    else:
                        arcpy.AddMessage("Feature Class is not a Point nor Polyline.")
                        #Logging
                        #log.logTrace("Feature Class is not a Point nor Polyline")
                except:
                    print traceback.format_exc()
                    #log.logTrace(traceback.format_exc())
            else:
                print "No return measure values"
            ucur.updateRow(urow)


def cleanWorkspace():
    for i in os.listdir(wkspace):
        try:
            os.remove(wkspace + "\\" + i)
        except:
            arcpy.AddMessage("Could not delete file" + " - " + i)
            #log.logTrace("Could not delete file" + " - " + i)


def buildFields(fc):
    desc = arcpy.Describe(fc)
    if desc.shapeType == "Point":
        if eF.checkForField(fc, "MEAS") == 0:
            arcpy.AddField_management(fc, "MEAS", "DOUBLE", "", "")
    elif desc.shapeType == "Polyline":
        if eF.checkForField(fc, "FMEAS") == 0:
            arcpy.AddField_management(fc, "FMEAS", "DOUBLE", "", "")
        if eF.checkForField(fc, "TMEAS") == 0:
            arcpy.AddField_management(fc, "TMEAS", "DOUBLE", "", "")


def findPolylineToPolylineIntersectPointCount(fc1, fc2):
    inputfc = gpF.featureLayer(fc1)
    inputfc_intersect = inputfc.intersect(fc2, "Point")
    #arcpy.AddMessage("interesected: " + str(gpF.featureLayer(inputfc_intersect).count()))
    intersectedpoints = gpF.featureLayer(inputfc_intersect)
    return intersectedpoints


def getFeatureMeasureValue(fc, sql):
    try:
        switch = ""
        measureList = []
        fl = arcpy.CreateUniqueName(os.path.basename(fc), wkspace)
        arcpy.MakeFeatureLayer_management(fc, fl, sql)

        #getting measure values per record
        if arcpy.Describe(fl).shapeType == "Point":
            new_fl = fl
            props = "RID POINT MEAS"
            switch = "pointMe"
        elif arcpy.Describe(fl).shapeType == "Polyline":
            #arcpy.AddMessage(fl)
            intersectionresult = findPolylineToPolylineIntersectPointCount(fl, route)
            if intersectionresult.count() == 1:
                #polyline intersects in only one spot and should only have a measure
                new_fl = intersectionresult.path
                props = "RID POINT MEAS"
                switch = "pointMe"
            else:
                new_fl = fl
                props = "RID LINE FMEAS TMEAS"
                switch = "lineMe"
        else:
            #Logging
            #log.logTrace("Feature Class is not a Point/Polyline")
            arcpy.AddMessage("Feature Class is not a Point/Polyline")
            print new_fl

        measureTable = arcpy.CreateUniqueName("measTable", wkspace)
        arcpy.LocateFeaturesAlongRoutes_lr(new_fl, route, "SERIES", 1, measureTable, props)
        if int(arcpy.GetCount_management(measureTable).getOutput(0)) > 0:
            rows = arcpy.SearchCursor(measureTable)
            for row in rows:
                if switch == "pointMe":
                    measureList.append(row.MEAS)
                elif switch == "lineMe":
                    measureList.append(row.FMEAS)
                    measureList.append(row.TMEAS)
                else:
                    #Logging
                    pass
                    #log.logTrace("Switch variable was not set in the code above")
        else:
            #log.logTrace(fc + " -- " + str(int(arcpy.GetCount_management(measureTable).getOutput(0))))
            measureList = [00000, 00000]
        #arcpy.AddMessage("here" + str(measureList))

        #log.logTrace(str(measureList))
        arcpy.Delete_management(fl)
        arcpy.AddMessage(measureList)
        return measureList


    except:
        #Logging
        arcpy.AddMessage(traceback.format_exc())
        #log.logTrace(traceback.format_exc())
        arcpy.Delete_management(fl)



if __name__ == "__main__":
    main()





