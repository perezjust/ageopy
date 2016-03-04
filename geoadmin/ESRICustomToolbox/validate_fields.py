import os, string, sys, traceback, shutil, logging
import arcpy


def main():


    try:

        fc = arcpy.GetParameter(0)
        validate_fields(fc)
    except:
        
        arcpy.AddMessage(traceback.format_exc())




def validate_fields(fc):
    arcpy.AddMessage(arcpy.Describe(fc).catalogPath)#.serviceProperties)
    arcpy.AddMessage(arcpy.Describe(fc).catalogPath.split(".sde")[0] + ".sde")
    workspace = arcpy.Describe(fc).catalogPath.split(".sde")[0] + ".sde"
    for i in arcpy.ListFields(fc):
        domain_name = i.domain
        if domain_name is not None:
            arcpy.AddMessage(domain_name)
            get_domain_values(domain_name, workspace)



def get_domain_values(domain_name, workspace):
    for dom in arcpy.da.ListDomains(workspace):
        arcpy.AddMessage(dom.name)


def filter_fields(table, fields):
    finallist = []
    for i in arcpy.ListFields(table):
        if i.name in fields:
            fldlist = [i.name, i.name, "VISIBLE None;"]
            #print " ".join(fldlist)
            finallist.append(" ".join(fldlist))
        else:
            fldlist = [i.name, i.name, "HIDDEN None;"]
            #print " ".join(fldlist)
            finallist.append(" ".join(fldlist))
    print " ".join(finallist)
        




if __name__ == "__main__":
    main()

