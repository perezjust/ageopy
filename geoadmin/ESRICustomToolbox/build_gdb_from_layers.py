import os, string, sys, traceback, shutil, logging, os.path, time
import arcpy



import expFuncs as eF
from expFuncs import *
import gpFuncs as gpF
from gpFuncs import *


def main():

    try:

        dbconn = arcpy.GetParameter(0)
        only_check_fields = arcpy.GetParameter(1)
        #get_gdb_schema(dbconn)
        #set_layer_name_from_gdb()
        layer_field_dict = build_layer_field_dict()
        find_deleteme_fields(dbconn, layer_field_dict, only_check_fields)


    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()


def find_deleteme_fields(dbconn, layer_field_dict, only_check_fields):
    for i in layer_field_dict:
        target_dataSource = build_target_arcpy_dataSource(dbconn, i)
        field_list = arcpy.ListFields(target_dataSource)
        for fld in field_list:
            #arcpy.AddMessage(target_dataSource)
            if fld.name not in layer_field_dict[i]:
                if only_check_fields == True:
                    arcpy.AddMessage(fld.name)
                else:
                    try:
                        arcpy.DeleteField_management(target_dataSource, fld.name)
                    except:
                        arcpy.AddMessage(str(target_dataSource) + " did not delete field --> " + str(fld.name))
        #arcpy.AddMessage(layer_field_dict[i])
        #arcpy.AddMessage(build_target_arcpy_dataSource(dbconn, i))

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
        #arcpy.AddMessage(i.datasetName)
        dsc_layer = arcpy.Describe(i)
        field_info = dsc_layer.fieldInfo
        for index in xrange(0, field_info.count):
            if field_info.getVisible(index) == "VISIBLE":
                #arcpy.AddMessage("\tVisible: {0}".format(field_info.getVisible(index)))
                #arcpy.AddMessage("\tVisible: {0}".format(field_info.getFieldName(index)))
                layer_field_dict[str(i.dataSource)].append(str(field_info.getFieldName(index)))
    arcpy.AddMessage(layer_field_dict)
    return layer_field_dict




def get_dataframe(switch):
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd, mxd.activeDataFrame.name)[0]
    return df


def set_layer_name_from_gdb():
    df = get_dataframe()
    layer_list = arcpy.mapping.ListLayers(mxd, "", df)
    for i in layer_list:
        i.name = i.datasetName
    mxd.save()
    arcpy.RefreshTOC()


def get_gdb_schema(dbconn):
    df = get_dataframe()
    feature_dataset_list = []
    layer_list = arcpy.mapping.ListLayers(mxd, "", df)
    for i in layer_list:
        if i.supports("DATASOURCE") is True:
            dataset_name = i.dataSource.split("\\")[-2].split(".")[-1]
            feature_class_name = str(i.datasetName).split(".")[-1]
            arcpy.CopyFeatures_management(i, str(dbconn) + "\\" + val + "\\" + valname)
##            #arcpy.AddMessage(val)
##            if val not in feature_dataset_list:
##                feature_dataset_list.append(val)
##    for ix in feature_dataset_list:
##        arcpy.AddMessage(ix)








if __name__ == "__main__":
    main()





