import os
import string
import sys
import traceback
import shutil
import logging
import os.path
import time
import arcpy
import arceditor


#sys.path.append(os.path.join(os.path.dirname(os.getcwd()), "esri"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "esri"))
import featurelayer
import mapdoc



def main():

    #Parameters
    fc = arcpy.GetParameterAsText(0)
    pauseTime = arcpy.GetParameterAsText(1)

    try:

        manager(fc, pauseTime)

        arcpy.AddMessage( "\r\n\r\n\r\n ***LOOK FOR A RESULTING FEATURE LAYER IN YOUR TABLE OF CONTENTS : EXPORT THE TEMP LAYER TO FILE IF NEEDED.\r\n\r\n\r\n")

    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()



def manager(fc, pauseTime):
    #featureLayer = gpF.featureLayer(fc)
    desc = arcpy.Describe(fc)
    shapefield = desc.ShapeFieldName

    for srow in arcpy.SearchCursor(fc):
        arcpy.AddMessage(str(srow.getValue(desc.OIDFieldName)))
        #feat = srow.getValue(shapefield).area
        feat = srow.shape

        extent = feat.extent
        arcpy.AddMessage(extent)
        zoom_to_layer(extent)
        time.sleep(float(pauseTime))


def zoom_to_layer(extent):
    mxd = arcpy.mapping.MapDocument("CURRENT")
    #arcpy.AddMessage(mxd.activeDataFrame)
    df = arcpy.mapping.ListDataFrames(mxd, mxd.activeDataFrame.name)[0]
    #arcpy.AddMessage(df.name)
    arcpy.AddMessage(extent)
    df.extent = extent
    df.scale = df.scale * 1.25
    arcpy.RefreshActiveView()



if __name__ == "__main__":
    main()





