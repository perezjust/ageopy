import os, string, sys, traceback, shutil, logging
import arcpy


def main():


    try:

        workspace = arcpy.GetParameter(0)
        domain_name = arcpy.GetParameter(1)
        domain_desc = arcpy.GetParameter(2)
        validate_fields(workspace, domain_name, domain_desc)
        
    except:
        
        arcpy.AddMessage(traceback.format_exc())



def validate_fields(workspace, domain_name, domain_desc):
    for de in arcpy.da.Walk(workspace):
        arpcy.AddMessage(de)



def validate_fields1():
    arcpy.AddMessage(arcpy.Describe(data_element).catalogPath)#.serviceProperties)
    arcpy.AddMessage(arcpy.Describe(data_element).catalogPath.split(".sde")[0] + ".sde")
    workspace = arcpy.Describe(data_element).catalogPath.split(".sde")[0] + ".sde"
    for i in arcpy.ListFields(data_element):
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

