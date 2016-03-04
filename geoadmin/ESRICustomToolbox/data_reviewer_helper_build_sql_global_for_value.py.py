import os, string, sys, traceback, shutil, logging
import arcpy



import expFuncs as eF
from expFuncs import *
import gpFuncs as gpF
from gpFuncs import *


def main():

    fc = arcpy.GetParameterAsText(0)
    value = arcpy.GetParameterAsText(1)
    data_type = arcpy.GetParameterAsText(2)
    
    try:

        buildSQL(fc, value, data_type)

    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()


def buildSQL(fc, value, data_type):
    field_obj_list = arcpy.ListFields(fc, "", data_type)
    field_list = []
    for i in field_obj_list:
        field_list.append(i.name + "='Unknown'")
    sql_query = " OR ".join(field_list)
    arcpy.AddMessage("\nSQL Query:")
    arcpy.AddMessage("============================================")
    arcpy.AddMessage(sql_query)
    arcpy.AddMessage("\n")
        
        

if __name__ == "__main__":
    main()
