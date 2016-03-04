import os
import string
import sys
import traceback
import shutil
import logging
import os.path
import arcpy



import expFuncs as eF
from expFuncs import *
import gpFuncs as gpF
from gpFuncs import *


def main():

    try:

        dbconn = arcpy.GetParameter(0)
        only_check_fields = arcpy.GetParameter(1)
        layer_field_dict = build_layer_field_dict()
        find_deleteme_fields(dbconn, layer_field_dict, only_check_fields)

    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()


def find_deleteme_fields(dbconn, layer_field_dict, only_check_fields):
    arcpy.AddMessage("\r\n\r\n")
    arcpy.AddMessage("See layers and fields to be deleted below.\r\n")
    arcpy.AddMessage("\r\n")
    for i in layer_field_dict:
        arcpy.AddMessage("###### ")
        arcpy.AddMessage("###### " + i)
        arcpy.AddMessage("###### Fields To Delete From the Above Layer:")
        arcpy.AddMessage("###### ")
        target_dataSource = build_target_arcpy_dataSource(dbconn, i)
        field_list = arcpy.ListFields(target_dataSource)
        for fld in field_list:
            if fld.name not in layer_field_dict[i]:
                if only_check_fields == True:
                    arcpy.AddMessage(fld.name)
                else:
                    try:
                        arcpy.DeleteField_management(target_dataSource, fld.name)
                        arcpy.AddMessage("DELETED " + str(fld.name))
                    except:
                        arcpy.AddMessage(str(target_dataSource) + " did not delete field --> " + str(fld.name))


def build_target_arcpy_dataSource(dbconn, src_dataSource):
    dataset_name = src_dataSource.split("\\")[-2].split(".")[-1]
    feature_class_name = src_dataSource.split("\\")[-1].split(".")[-1]
    target_dataSource = str(dbconn) + "\\" + dataset_name + "\\" + feature_class_name
    return target_dataSource


def build_layer_field_dict():
    from collections import defaultdict
    layer_field_dict = defaultdict(list)
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd, mxd.activeDataFrame.name)[0]
    layer_list = arcpy.mapping.ListLayers(mxd, "", df)
    for i in layer_list:
        dsc_layer = arcpy.Describe(i)
        field_info = dsc_layer.fieldInfo
        for index in xrange(0, field_info.count):
            if field_info.getVisible(index) == "VISIBLE":
                layer_field_dict[str(i.dataSource)].append(str(field_info.getFieldName(index)))
    return layer_field_dict


if __name__ == "__main__":
    main()





