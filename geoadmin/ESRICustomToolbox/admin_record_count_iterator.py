import os
import string
import sys
import traceback
import shutil
import logging
import arcpy


def main():


    try:

        workspace = arcpy.GetParameter(0)
        recursive = arcpy.GetParameter(1)
        iterate_items(workspace)
		
    except:
        
        arcpy.AddMessage(traceback.format_exc())


def iterate_items(workspace):
    arcpy.env.workspace = workspace
    itemlist = []
    for fc in arcpy.ListFeatureClasses():
        itemlist.append(fc)
    for table in arcpy.ListTables():
        itemlist.append(table)
    for i in itemlist:
        arcpy.AddMessage(os.path.basename(i) + " -- " + str(int(arcpy.GetCount_management(i).getOutput(0))))





if __name__ == "__main__":
    main()

