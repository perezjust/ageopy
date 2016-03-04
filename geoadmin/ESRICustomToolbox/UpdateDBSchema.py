import arcpy
import os, string, sys, traceback
from os.path import join


import expFuncs as expF
from expFuncs import *
import gpFuncs as gpF
from gpFuncs import *



def main():

        exp = meiSetUp("updateDBSchema")
        log = logIt(exp.logPath)
        

        #deleteObjectJob(log)
        try:
                log.logMessageHeader("Script started")
                createObjectJob(log)
                log.logMessageHeader("Script stopped")
                
        except:
                log.logTrace(traceback.format_exc())





def readConfig():
     pass   
        



def createObjectJob(log):
        destinationdict =
                {

                update + "\\" + "Civil_Points.shp" :
                wkspace + "Civil_Survey_Points"

                }

        for source in destinationdict:
            try:
                    
                createFeatureClass(source, destinationdict[source])

            except:
                log.logTrace(traceback.format_exc())



def deleteObjectJob(log):
        deletelist = [

                r"Blah"

                ]

        for dl in deletelist:

            try:
                
                deleteFeatureClass(dl)
    
            except:
                log.logTrace(traceback.format_exc())


def deleteFieldsJob():
        '''
                Separate fields by "@" for multiple fields to be deleted.
        '''
        deletedict = {

        r"SomeConnectionStuff.SDE.Working_Geotechinical_Bore_Holes":
        "LAT@LONG",

        r"SomeConnectionStuff.SDE.Working_Fittings_Horizontal":
        "NORTHING@EASTING",

        r"SomeConnectionStuff.SDE.Working_Valves":
        "LAT@LONG"

        }

        deleteFields(deletedict)


def deleteFields(fc_dict):
        for fc in fc_dict:
                fieldlist = fc_dict[fc].split("@")
                for field in fieldlist:
                        arcpy.DeleteField_management(fc, field)


def createFeatureClass(src, dst):
        if arcpy.Exists(dst):
                deleteFeatureClass(dst)
        arcpy.env.workspace = os.path.dirname(dst)
        print os.path.dirname(dst) + "---" + os.path.basename(dst).split(".")[2]
        arcpy.CopyFeatures_management(src, os.path.basename(dst).split(".")[2])


def deleteFeatureClass(fc):
    arcpy.Delete_management(fc)


if __name__ == "__main__":
    main()


