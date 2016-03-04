import arcpy
import os, string, sys, traceback
from os.path import join
from collections import defaultdict


import expFuncs as expF
from expFuncs import *
import gpFuncs as gpF
from gpFuncs import *

exp = meiSetUp("compareFields")

#Parameters
comp_with = arcpy.GetParameter(0)
comp_against = arcpy.GetParameter(1)

def main():
    try:
        arcpy.AddMessage("Starting...")
        func1()
    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()



def func1():
    flds_comp_with = fieldNameList(comp_with)
    flds_type_comp_with = fieldTypeDict(comp_with)
    flds_comp_against = fieldNameList(comp_against)
    flds_type_comp_against = fieldTypeDict(comp_against)

    my_result = compareFields(flds_comp_with, flds_type_comp_with, flds_comp_against, flds_type_comp_against)
    formatReturn(my_result)
    #arcpy.AddMessage(my_result)


def formatReturn(inDictio):

    arcpy.AddMessage("\n\n")

    arcpy.AddMessage("Existing Data: " + str(comp_with))
    arcpy.AddMessage("\n")
    arcpy.AddMessage("New Data: " + str(comp_against))
    arcpy.AddMessage("\n\n")

    arcpy.AddMessage("===============================")
    arcpy.AddMessage("Matching Fields:")
    arcpy.AddMessage("- - - - - - - - - - - - - - - -")
    for k,v in inDictio.items():
        if v == 'full_match':
            arcpy.AddMessage(k)

    arcpy.AddMessage("===============================")
    arcpy.AddMessage("Data Types Do Not Match:")
    arcpy.AddMessage("- - - - - - - - - - - - - - - -")
    for k,v in inDictio.items():
        if v == 'semi_match':
            arcpy.AddMessage(k)

    arcpy.AddMessage("===============================")
    arcpy.AddMessage("Not in " + str(comp_with) + ":")
    arcpy.AddMessage("- - - - - - - - - - - - - - - -")
    for k,v in inDictio.items():
        if v == 'under':
            arcpy.AddMessage(k)

    arcpy.AddMessage("===============================")
    arcpy.AddMessage("Not in " + str(comp_against) + ":")
    arcpy.AddMessage("- - - - - - - - - - - - - - - -")
    for k,v in inDictio.items():
        if v == 'over':
            arcpy.AddMessage(k)

    arcpy.AddMessage("\n\n")



def compareFields(inList1, inDictio1, inList2, inDictio2):
    match_dictio = {}
    for i in inList1:
        if i in inList2:#At least partial match here
            if inDictio1[i] == inDictio2[i]:
                match_dictio[i] = "full_match"
            else:
                match_dictio["Existing: " + i + " - " + inDictio1[i] + " | New: " + i + " - " + inDictio2[i] ] = "semi_match"
        else:
            match_dictio[i] = "over"
    del i
    for j in inList2:
        if j not in inList1:
            match_dictio[j] = "under"
    return match_dictio


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
