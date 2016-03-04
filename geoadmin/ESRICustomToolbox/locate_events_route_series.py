import os, string, sys, traceback, shutil, logging, os.path
import arcpy



import expFuncs as eF
from expFuncs import *
import gpFuncs as gpF
from gpFuncs import *


#Setup
exp = meiSetUp("locate_event_route_series")
#log = logIt(exp.log_path)
#wkspace = exp.wkspacePath
arcpy.env.overwriteOutput = True


def main():

    try:
        fc = arcpy.GetParameterAsText(0)
        rid_field = arcpy.GetParameterAsText(1)
        event_table = arcpy.GetParameter(2)
        event_table_field = arcpy.GetParameter(3)

        func1(fc, rid_field, event_table, event_table_field)

    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()
        log.logTrace(traceback.format_exc())


def find_marker2(event_table, event_table_field):
    dup_list = []
    measure_list = []
    fields = arcpy.ListFields(event_table)
    field_list = []
    field_list.append(str(event_table_field))
    for fld in fields:
        if fld.name <> str(event_table_field):
            field_list.append(str(fld.name))
    for i in arcpy.da.SearchCursor(event_table, field_list):
        if i[0] in measure_list:
            dup_list.append(i[0])

        measure_list.append(i[0])
##        measure_dict.append
    if len(dup_list) > 0:
        arcpy.AddMessage("You had these values more than once in your input.  The resulting attribute chaining, with these duplicate inputs, is suspect.  You could remove duplicates, which should then produce a reliabe result or check on the attributes of the values in the list.\r\n")
        arcpy.AddMessage(dup_list)
    return measure_list


def func1(fc, rid_field, event_table, event_table_field):
    lyr_mileposts = arcpy.CreateUniqueName("lyr_mileposts", "in_memory")
    final = assign_mileposts_to_routes(fc, rid_field, event_table, event_table_field)
    table = build_spacing_table(final)
    arcpy.MakeRouteEventLayer_lr(fc, rid_field, table, "expRID POINT MEASURE", lyr_mileposts, "", "", "")
    arcpy.SetParameter(4, lyr_mileposts)


def assign_mileposts_to_routes(fc, rid_field, event_table, event_table_field):
    mvalues = find_mvalue_segments(fc, rid_field)
    milepost_values = find_marker2(event_table, event_table_field)
    from collections import defaultdict
    mileposts = defaultdict(list)
    for x in milepost_values:
        for k in mvalues:
            for m, n in mvalues[k]:
                if m <= x <= n:
                    mileposts[x].append(k)
    return mileposts


def find_mvalue_segments(fc, rid_field):
    from collections import defaultdict
    mvalues = defaultdict(list)
    for i in arcpy.SearchCursor(fc):
        tag = i.getValue(rid_field)
        start = i.shape.extent.MMin
        end = i.shape.extent.MMax
        mvalues[tag].append((start, end))
        #print (str(i.shape.extent.MMin) + " - " + str(i.shape.extent.MMax) + " - " + str(i.getValue("Series")))
    return mvalues


def build_spacing_table(final_list):
    table = arcpy.CreateTable_management("in_memory", "mp_table")
    arcpy.AddField_management(table, "expRID", "TEXT", field_length=50)
    arcpy.AddField_management(table, "DUPLICATE", "TEXT", field_length=50)
    arcpy.AddField_management(table, "MEASURE", "DOUBLE")
    icur = arcpy.da.InsertCursor(table, ("expRID", "MEASURE", "DUPLICATE"))
    for key in final_list:
        dup = "no"
        if len(final_list[key]) > 1:
            dup ="yes"
        for value in final_list[key]:
            print key, value
            icur.insertRow((str(value), str(key), dup))
    return table



if __name__ == "__main__":
    main()
