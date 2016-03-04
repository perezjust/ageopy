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


#Setup
exp = meiSetUp("mp_gen_equations")
#log = logIt(exp.log_path)
#wkspace = exp.wkspacePath
arcpy.env.overwriteOutput = True


def main():

    try:
        fc = arcpy.GetParameterAsText(0)
        rid_field = arcpy.GetParameterAsText(1)
        spacing = arcpy.GetParameter(2)
        create_begin_point = arcpy.GetParameter(4)
        create_end_point = arcpy.GetParameter(5)
        
        func1(fc, spacing, rid_field, create_begin_point, create_end_point)

    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()
        #log.logTrace(traceback.format_exc())



def func1(fc, spacing, rid_field, create_begin_point, create_end_point):
    lyr_mileposts = arcpy.CreateUniqueName("lyr_mileposts", "in_memory")
    final = assign_mileposts_to_routes(fc, spacing, rid_field, create_begin_point, create_end_point)
    table = build_spacing_table(final)
    arcpy.MakeRouteEventLayer_lr(fc, rid_field, table, "mpmID POINT mpmLength", lyr_mileposts, "", "", "")
    arcpy.SetParameter(3, lyr_mileposts)



def assign_mileposts_to_routes(fc, spacing, rid_field, create_begin_point, create_end_point):
    mvalues = find_mvalue_segments(fc, rid_field)
    endvalues = find_ends(mvalues)
    milepost_values = generate_mp_values(endvalues[0], endvalues[1], spacing, create_begin_point, create_end_point)
    arcpy.AddMessage(milepost_values)
    from collections import defaultdict
    mileposts = defaultdict(list)
    #for milepost number in mileposts
    for x in milepost_values:
        #for route series in total route series
        for k in mvalues:
            # for to and from in route series
            for m, n in mvalues[k]:
                if m <= x <= n:
                    mileposts[x].append(k)
    return mileposts



def generate_mp_values(minval, maxval, spacing, create_begin_point, create_end_point):
    mileposts = []
    r = minval
    if create_begin_point == "true":
        mileposts.append(r)
    while r < maxval:
        r += float(spacing)
        mileposts.append(r)
    if create_end_point == "true":
        if maxval not in mileposts:
            mileposts.append(maxval)
    return mileposts



def find_ends(mvalues):
    sorted_dict = sorted(mvalues.iteritems(), key=lambda (k,v): v[0], reverse=False)
    minval = sorted_dict[0][-1][-1][0]
    minval_integer = minval
    minval_worker = str(minval).split(".")
    if len(minval_worker) > 1:
        minval_integer = int(minval_worker[0]) + 1
    maxval = sorted_dict[-1][-1][-1][-1]
    arcpy.AddMessage(minval)
    arcpy.AddMessage(minval_integer)
    arcpy.AddMessage(maxval)
    return [minval_integer, maxval]



def find_mvalue_segments(fc, rid_field):
    from collections import defaultdict
    mvalues = defaultdict(list)
    for i in arcpy.SearchCursor(fc):
        tag = i.getValue(rid_field)
        start = i.shape.extent.MMin
        end = i.shape.extent.MMax
        mvalues[tag].append((start, end))
    arcpy.AddMessage(mvalues)
    return mvalues


def build_spacing_table(final_list):
    table = arcpy.CreateTable_management("in_memory", "mp_table")
    arcpy.AddField_management(table, "mpmId", "TEXT", field_length=50)
    arcpy.AddField_management(table, "Duplicate", "TEXT", field_length=50)
    arcpy.AddField_management(table, "mpmLength", "DOUBLE")
    icur = arcpy.da.InsertCursor(table, ("mpmId", "mpmLength", "Duplicate"))
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
