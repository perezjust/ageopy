import arcpy
import os
import string
import sys
import traceback
from os.path import join
from collections import defaultdict




def main():
    try:

        """
            r"O:\AppData\GIS\Commercial\HoustonGIS\RexTag 1018 Release"
            folder call:
            comp_with = build_item_list(r"O:\AppData\GIS\Commercial\HoustonGIS\RexTag 1018 Release", "shp")
        """
        
        comp_target_path = r"Database Connections\GISCloudQA_background_os.sde\background.GIS.Rextag"
        comp_with_items = build_item_list(comp_target_path)
        
        comp_against_path = r"O:\AppData\GIS\Cloud\Data\Commercial\RexTag 1021 Release"
        compare_items(comp_with_items, comp_against_path)
        
    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()



def build_item_list(target_workspace, search_filter=None):
    allfiles = []
    if search_filter == None:
        arcpy.env.workspace = target_workspace
        allfiles = [fc.split(".")[-1] for fc in arcpy.ListFeatureClasses()]
    else:
        for root,dir,files in os.walk(target_workspace):
                    filelist = [ os.path.join(root,fi) for fi in files if fi.endswith(search_filter)]
                    for f in filelist:
                            allfiles.append(os.path.basename(f)[:-4])
    return allfiles



def compare_items(comp_with_items, comp_against):
    found_list = []
    notfound_list =[]
    arcpy.env.workspace = comp_against
    #fcs = [fc.split(".")[-1] for fc in arcpy.ListFeatureClasses()]
    fcs = build_item_list(comp_against, "shp")
    for fc in fcs:
        if fc in comp_with_items:
            found_list.append(fc)
        else:
            notfound_list.append(fc)
    print "Found Count: " + str(len(found_list))
    print found_list
    print "Not Found Count: " + str(len(notfound_list))
    print notfound_list
    print "Target Count: " + str(len(fcs))







if __name__ == "__main__":
    main()










