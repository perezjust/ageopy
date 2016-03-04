import arcpy
import os, string, sys, traceback, ast
from os.path import join


import expFuncs as eF
from expFuncs import *


#parameters
lineFeature = arcpy.GetParameterAsText(0)
pointField2 = arcpy.GetParameterAsText(1)
pointFeature = arcpy.GetParameterAsText(2)
pointField1 = arcpy.GetParameterAsText(3)
bufferDistance = arcpy.GetParameterAsText(4)
ignoreValues = arcpy.GetParameterAsText(5)

arcpy.AddMessage("BANG")

def main():
    sde = r"SomeConnectionFile.sde"


    try:


        firstFunc()



    except:
        arcpy.AddMessage(traceback.format_exc())





########FUNCTIONS#########


def firstFunc():

    try:
        ignoreValues_list = listUniJazz(ignoreValues)
        newBufferDistance = 0
        if bufferDistance != "":
            newBufferDistance = bufferDistance
        #fieldList = [pointField1, pointField2, pointField3]
        desc = arcpy.Describe(lineFeature)
        if desc.hasOID == 1:
            shapefield = desc.ShapeFieldName
            oidField = desc.OIDFieldName
            arcpy.MakeFeatureLayer_management(pointFeature, "pointFeature")
            scur = arcpy.UpdateCursor(lineFeature)
            for srow in scur:
                objId = str(srow.getValue(oidField))
                sqlHas = '"' + oidField + '"' + " = " + objId
                arcpy.MakeFeatureLayer_management(lineFeature, "lineFeature" + objId, sqlHas)
                arcpy.SelectLayerByLocation_management("pointFeature", "INTERSECT", "lineFeature" + objId, newBufferDistance)
                values = []
                arcpy.AddMessage(sqlHas + "---->" + str(int(arcpy.GetCount_management("pointFeature").getOutput(0))))
                if int(arcpy.GetCount_management("pointFeature").getOutput(0)) > 0:
                    if int(arcpy.GetCount_management("pointFeature").getOutput(0)) == 1:
                        arcpy.AddMessage(sqlHas + "---->" + str(int(arcpy.GetCount_management("pointFeature").getOutput(0))))
                    pointSelectionCursor = arcpy.SearchCursor("pointFeature")
                    arcpy.AddMessage(ignoreValues_list)
                    for selectedRow in pointSelectionCursor:
                        #Iterating the selected features in the point file to find common values
                        selectedRowValue = str(selectedRow.getValue(pointField1))
                        if selectedRowValue not in ignoreValues_list and selectedRowValue != '0.0':
                            arcpy.AddMessage(selectedRowValue)
                            values.append(selectedRowValue)
                    value = findCommonValue(values)
                    #arcpy.AddMessage(sqlHas + "... " + value)
                    #arcpy.AddMessage(values)

                    srow.setValue(pointField2, value)
                    scur.updateRow(srow)

                else:
                    pass
                    #arcpy.AddMessage(sqlHas + "---->" + str(int(arcpy.GetCount_management("pointFeature").getOutput(0))))


        else:
            arcpy.AddMessage("This tool requires that the input feature class has an ObjectID field.")
    except:
        arcpy.AddMessage(traceback.format_exc())


def listUniJazz(inlist):
    s1 = inlist.split(",")
    s = [ item.encode('ascii') for item in s1 ]
    return s

def findCommonValue(values):
    if len(values) > 0:
        d = {}
        for i in set(values):
            d[i] = values.count(i)
        counter = 0
        for key, value in sorted(d.iteritems(), key=lambda (k,v): (v,k), reverse=True):
            if counter == 0:
                value1 = key
                counter += 1
    else:
        value1 = ""
    return value1




if __name__ == "__main__":
    main()
