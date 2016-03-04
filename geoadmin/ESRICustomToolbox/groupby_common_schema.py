import arcpy
import os, string, sys, traceback
from os.path import join
from collections import defaultdict


import expFuncs as expF
from expFuncs import *
import gpFuncs as gpF
from gpFuncs import *

exp = meiSetUp("compareFields")


def main():
    try:
        arcpy.AddMessage("Starting...")

        table_list = arcpy.GetParameter(0)
        func1(table_list)

    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()



def func1(table_list):
    master_dict = {}
    for i in table_list:
        flds_list = fieldNameList(i)
        flds_dict = fieldTypeDict(i)
        master_dict[i] = flds_dict
    compare_dicts(master_dict)


def compare_dicts(master_dict):
    arcpy.AddMessage(len(master_dict))
    match_list = []
    total_list = []
    for i in master_dict:
        i_matched = []
        #looping over entire dict
        for j in master_dict:
            if j not in match_list:
                if master_dict[i] == master_dict[j]:
                    i_matched.append(os.path.basename(str(j)))
                    match_list.append(j)
        if len(i_matched) > 0:
            total_list.append(i_matched)
    arcpy.AddMessage(len(total_list))
    count_list = []
    for x in total_list:
        if len(x) > 1:
            arcpy.AddMessage(str(x) + "\n")
            count_list.append(len(x))
    for x in total_list:
        if len(x) == 1:
            arcpy.AddMessage(str(x) + "\n")
            count_list.append(len(x))
    arcpy.AddMessage(sum(count_list))


def fieldNameList(inTable):
    fldNameList = []
    for fi in arcpy.ListFields(inTable):
        fldNameList.append(fi.name)
    return fldNameList


def fieldTypeDict(inTable):
    dictio = {}
    for fi in arcpy.ListFields(inTable):
        dictio[fi.name] = fi.type
    return dictio


if __name__ == "__main__":
    main()
