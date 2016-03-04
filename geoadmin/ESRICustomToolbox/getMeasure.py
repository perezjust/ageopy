import os, string, sys, traceback, shutil, logging
import arcpy



import expFuncs as eF
from expFuncs import *


inPoint = arcpy.GetParameterAsText(0)

#inRoute = arcpy.GetParameterAsText(1)
#createOutput = arcpy.GetParameterAsText(2)
#coordpriority = arcpy.GetParameterAsText(2)

def main():


    try:

        getMeasure(inPoint)

    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()



def getMeasure(inPoint):
    try:
        locateFeatures = arcpy.CreateUniqueName("inPointLocated", "in_memory")
        arcpy.LocateFeaturesAlongRoutes_lr(inPoint, inRoute, "SERIES", "20 feet", locateFeatures, "RID POINT MEAS")
        scur = arcpy.SearchCursor(locateFeatures)
        arcpy.AddMessage("\n\n")
        arcpy.AddMessage("Measures down the line:\n")
        for srow in scur:
            arcpy.AddMessage("Point Number:" + str(srow.getValue("ObjectID")) + " | Station: "+ str("{0:.2f}".format(srow.getValue("MEAS"))) + " | Mile Post: " + str("{0:.2f}".format(srow.getValue("MEAS") / 5280)))
        arcpy.AddMessage("\n\n")

##        if createOutput == True:
##            arcpy.AddMessage("True")
##        else:
##            arcpy.AddMessage("False")
    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()






if __name__ == "__main__":
    main()
