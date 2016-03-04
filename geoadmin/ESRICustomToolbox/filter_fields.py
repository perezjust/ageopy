import os, string, sys, traceback, shutil, logging
import arcpy


def main():


    try:

        table = r"Database Connections\GISCloudDev_pods_gs_os.sde\pods_gs.GIS.Address"
        fields = ["ObjectID", "EventID"]
        filter_fields(table, fields)

    except:
        
        print traceback.format_exc()





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

