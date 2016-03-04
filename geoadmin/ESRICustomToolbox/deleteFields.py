import os, string, sys, traceback, shutil, logging, os.path
import arcpy


try:


    #Parameters
    fc = arcpy.GetParameterAsText(0)
    dropFields = arcpy.GetParameterAsText(1)


except:
    arcpy.AddMessage(traceback.format_exc())

def main():

    try:

        func1(fc, dropFields)

    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()



def func1(fc, dropFields):
    for i in dropFields:
        arcpy.DeleteField_management(fc, i)





if __name__ == "__main__":
    main()





