import os, string, sys, traceback, shutil, logging
import arcpy


def main():
    try:

        inMeasure = arcpy.GetParameterAsText(0)
        inLine = arcpy.GetParameterAsText(1)
        inField = "CL_ID"
        getStationPoint(inMeasure, inLine, inField)


    except:
        arcpy.AddMessage(traceback.format_exc())


def getStationPoint(inMeasure, inLine, inField):
    try:

        arcpy.env.overwriteOutput = True
        inTableMPTxtFile = createRouteTable(inMeasure, inField)
        lyrMilePosts = arcpy.CreateUniqueName("lyrMilePosts", "%scratchGDB%")
        params = str(inField) + " POINT mpmLength"
        arcpy.env.workspace = "%scratchGDB%"
        arcpy.MakeRouteEventLayer_lr(inLine, inField, inTableMPTxtFile,  params, lyrMilePosts, "", "", "")
        arcpy.CopyFeatures_management(lyrMilePosts, "%scratchGDB%" + "\\" + "lyrMilePost")

        arcpy.RefreshActiveView()

        zoomToLayer("%scratchGDB%" + "\\" + "lyrMilePost")


        arcpy.SetParameter(2, "%scratchGDB%" + "\\" + "lyrMilePost")
    except:
        arcpy.AddMessage(traceback.format_exc())


def createRouteTable(inMeasure, inField):
    '''
        Creates the table that will be used to build the route event
    '''
    arcpy.env.overwriteOutput = True
    inTableMPTxtFile = arcpy.CreateUniqueName("inTableMP", "%scratchGDB%")
    arcpy.CreateTable_management("%scratchGDB%", os.path.basename(inTableMPTxtFile))
    arcpy.AddField_management(inTableMPTxtFile, inField, "Text", "", "")
    arcpy.AddField_management(inTableMPTxtFile, "mpmLength", "Long", "", "")
    icur = arcpy.InsertCursor(inTableMPTxtFile)
    irow = icur.newRow()
    irow.setValue(inField, "KHL")
    irow.mpmLength = inMeasure
    icur.insertRow(irow)
    return inTableMPTxtFile


def zoomToLayer(lyr):
    mxd = arcpy.mapping.MapDocument("CURRENT")
    #arcpy.AddMessage(mxd.activeDataFrame)
    df = arcpy.mapping.ListDataFrames(mxd, mxd.activeDataFrame.name)[0]
    #arcpy.AddMessage(df.name)
    activeLyrDescr = arcpy.Describe(lyr)
    arcpy.AddMessage(activeLyrDescr)
    activeLyrExtent = activeLyrDescr.extent
    arcpy.AddMessage(activeLyrExtent)
    df.extent = activeLyrExtent
    df.scale = df.scale * .25
    arcpy.RefreshActiveView()


if __name__ == "__main__":
    main()

