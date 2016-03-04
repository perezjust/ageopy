import arcpy
import os, string, sys, traceback
from os.path import join


import expFuncs as expF
from expFuncs import *
import gpFuncs as gpF
from gpFuncs import *


def main():

    try:
        
        dbconn = arcpy.GetParameter(0)
        func1(dbconn)
        

    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()


def func1(dbconn):
    arcpy.env.workspace = dbconn
    for i in arcpy.ListDatasets():
        try:
            
            datasetVersioned = arcpy.Describe(i).isVersioned
            if datasetVersioned == False:
                arcpy.AddMessage(str(i) + " version status is " + str(datasetVersioned))

        except:
            arcpy.AddMessage(traceback.format_exc())
            print traceback.format_exc()
    
    for j in arcpy.ListTables():
        try:
            
            tableVersioned = arcpy.Describe(j).isVersioned
            if tableVersioned == False:
                arcpy.AddMessage(str(j) + " version status is " + str(tableVersioned))

        except:
            arcpy.AddMessage(traceback.format_exc())
            print traceback.format_exc()



if __name__ == "__main__":
    main()
