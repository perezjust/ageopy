import os, string, sys, traceback, shutil, logging
import arcpy



import expFuncs as eF
from expFuncs import *
import gpFuncs as gpF
from gpFuncs import *




exp = meiSetUp("calculateType")
log = logIt(exp.logPath)
#wkspace = exp.wkspacePath
wkspace = "in_memory"

in_folder = arcpy.GetParameter(0)
in_field = arcpy.GetParameterAsText(1)
onlycheckforfield = arcpy.GetParameterAsText(2)

def main():


    try:

        #walk and build list of feature paths
        esrifolder = gpF.ESRI_FolderBrowser(in_folder)
        in_features = esrifolder.build_fs_catalog()


        #Get a list of feature classes that have the input field
        faillist = test_for_fields(in_features, in_field)
        arcMessage(arcpy.env.workspace)

        if not len(faillist) == 0:
            arcMessage("These inputs already have the field: " + in_field)
            for faillist_item in faillist:
                arcpy.AddMessage(faillist_item)

            '''I know this is ugly
            '''
            arcMessage("\n")
            arcMessage("Ignore the wizardy belowwwww.....")
            arcMessage("\n")
            arcMessage("==================================================")
            sys.exit()

        arcMessage("The field: " + str(in_field) + "   ..is not present.")

        if onlycheckforfield == "false":
            for in_fc in in_features:

                buildFields(in_fc, in_field)
                calcFields(in_fc, in_field)


    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()
        #Logging
        log.logTrace(traceback.format_exc())


def test_for_fields(in_features, fieldname):
    faillist = []
    for in_fc1 in in_features:
        if not eF.checkForField(in_fc1, fieldname) == 0:
            faillist.append(in_fc1)
    return faillist

def caller(in_features):
    for in_fc in in_features:
            calcFields(in_fc, in_field)

def buildFields(fc, fieldname):
    arcpy.AddField_management(fc, fieldname, "TEXT", "", "")


def calcFields(fc, fieldname):
    desc = arcpy.Describe(fc)
    goodname = desc.name
    if str(desc.name)[-4:] == ".shp":
        goodname = str(desc.name)[:-4]
    arcpy.CalculateField_management(desc.catalogPath, fieldname, '"' + goodname + '"', "PYTHON")




if __name__ == "__main__":
    main()





