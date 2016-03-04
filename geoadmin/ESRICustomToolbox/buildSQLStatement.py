import os, string, sys, traceback, shutil, logging
import arcpy



import expFuncs as eF
from expFuncs import *
import gpFuncs as gpF
from gpFuncs import *



fc = arcpy.GetParameterAsText(0)
field = arcpy.GetParameterAsText(1)


exp = meiSetUp("calculateMeasures")
log = logIt(exp.log_path)
wkspace = "in_memory"

def main():


    try:
        desc = arcpy.Describe(fc)
        if "Table" in str(desc.dataType):
            build_sql_for_table(fc, field)
        else:
            buildSQL(fc, field)


    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()
        #Logging
        log.logTrace(traceback.format_exc())


def build_sql_for_table(fc, field):
    querylist = gpF.make_table_querylist_unique(fc, field)
    arcpy.AddMessage("****************************************\n")
    arcpy.AddMessage(field +'"' + " IN ('" +  "','".join(querylist) + "')\n")
    arcpy.AddMessage("****************************************\n")


def buildSQL(fc, field):
    fcLayer = gpF.featureLayer(fc)
    queryList = fcLayer.makeQueryListUnique(field)
    arcpy.AddMessage("****************************************\n")
    arcpy.AddMessage(field + " IN (" + "','".join(queryList) + ")\n")
    #arcpy.AddMessage(field + " IN (" + str(queryList) + ")\n")
    arcpy.AddMessage("****************************************\n")







if __name__ == "__main__":
    main()





