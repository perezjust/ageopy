import os, string, sys, traceback, shutil, logging, os.path
import arcpy



import expFuncs as eF
from expFuncs import *
import gpFuncs as gpF
from gpFuncs import *

try:


    #Parameters
    fc = arcpy.GetParameterAsText(0)
    featureid = arcpy.GetParameterAsText(1)
    first_and_last1 = arcpy.GetParameterAsText(3)


    #Setup
    exp = meiSetUp("crossingsTable")
    log = logIt(exp.log_path)
    #wkspace = exp.wkspacePath
    arcpy.env.overwriteOutput = True

except:
    arcpy.AddMessage(traceback.format_exc())

def main():

    try:

        func1(fc, featureid, first_and_last1)

        arcpy.AddMessage( "\r\n\r\n\r\n ***LOOK FOR A RESULTING FEATURE LAYER IN YOUR TABLE OF CONTENTS : EXPORT THE TEMP LAYER TO FILE IF NEEDED.\r\n\r\n\r\n")

    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()
        log.logTrace(traceback.format_exc())



def func1(fc, featureid, first_and_last1):
    featureLayer = gpF.featureLayer(fc)
    points = featureLayer.featureVerticesToPoints(featureid, "", first_and_last1)
    #points = featureLayer.feature_vertices_to_points()
    arcpy.SetParameter(2, points)





if __name__ == "__main__":
    main()





