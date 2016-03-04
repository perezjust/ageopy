import os
import string
import sys
import shutil
import traceback
from os.path import join
from collections import defaultdict

import arcpy
import arceditor

import datastore



class DataElement(object):

    def __init__(self, path):
        self.path = path
        self.storetype = datastore.DataStore(path).storetype
        self.fieldnamelist = DataElement._listfields(self)

    def _get_sde_connection_path(self):
        pass

    def _listfields(self, fieldobjects=None):
        fldnamelist = []
        for fi in arcpy.ListFields(self.path):
            if fieldobjects == True:
                fldnamelist.append(fi)
            else:
                fldnamelist.append(fi.name)
        return fldnamelist


class GDBElement(DataElement):

    def __init__(self, path):
        DataElement.__init__(self, path)
        self.gdbobjectflatname = GDBElement._gdbobjectflatname(self)
        self.gdbrootpath, self.datastoretype = GDBElement._gdbrootpath(self)
        self.connectionpath = GDBElement._connectionpath(self)

    def _connectionpath(self):
        pathlist = self.path.split(".sde")
        return pathlist[0] + ".sde"

    def _list_codeddomains(self):
        codeddomainlist = []
        for i in GDBElement._listfields(self, True):
            codeddomainlist.append(i.domain)
        return codeddomainlist

    def _gdbrootpath(self):
        minus1item = self.path.split("\\")[-1]
        minus2item = self.path.split("\\")[-2]
        minus3item = self.path.split("\\")[-3]
        gdbrootpath = ""
        datastoretype = ""
        if minus1item.endswith(".sde"):
            gdbrootpath = self.path
            datastoretype = "sde"
        elif minus2item.endswith(".sde"):
            gdbrootpath = "\\".join(self.path.split("\\")[:-1])
            datastoretype = "sde"
        elif minus3item.endswith(".sde"):
            gdbrootpath = "\\".join(self.path.split("\\")[:-2])
            datastoretype = "sde"
        elif minus1item.endswith(".gdb"):
            gdbrootpath = self.path
            datastoretype = "gdb"
        elif minus2item.endswith(".gdb"):
            gdbrootpath = "\\".join(self.path.split("\\")[:-1])
            datastoretype = "gdb"
        elif minus3item.endswith(".gdb"):
            gdbrootpath = "\\".join(self.path.split("\\")[:-2])
            datastoretype = "gdb"
        return gdbrootpath, datastoretype



    def funckedup(self):
        if self.storetype == "sde":
            gdbrootpath = self.path.split(".sde")[0] + ".sde"
        elif self.storetype == "gdb":
            if minus2item.endswith(".gdb"):
                #located at root of gdb
                gdbrootpath = minus1item
            elif minus3item.endswith(".gdb"):
                dataset = minus2item
                gdbrootpath = dataset + "\\" + minus1item
        return gdbrootpath



    def _gdbobjectflatname(self):
        flatname = ""
        minus1item = self.path.split("\\")[-1]
        minus2item = self.path.split("\\")[-2]
        minus3item = self.path.split("\\")[-3]
        if self.storetype == "sde":
            if minus2item.endswith(".sde"):
                #located at root of gdb
                flatname = minus1item.split(".")[-1]
            elif minus3item.endswith(".sde"):
                dataset = minus2item.split(".")[-1]
                flatname = dataset + "\\" + minus1item.split(".")[-1]
        elif self.storetype == "gdb":
            if minus2item.endswith(".gdb"):
                #located at root of gdb
                flatname = minus1item
            elif minus3item.endswith(".gdb"):
                dataset = minus2item
                flatname = dataset + "\\" + minus1item
        return flatname

    def comparefields(self, compareitem):
        '''
            
        '''
        flds_comp_with = self.fieldnamelist
        flds_type_comp_with = GDBElement._fieldtypedict(self, self.path)
        flds_comp_against = GDBElement._fieldnamelist(compareitem)
        flds_type_comp_against = GDBElement._fieldtypedict(compareitem)
        my_result = _comparefieldshelper(flds_comp_with, flds_type_comp_with, flds_comp_against, flds_type_comp_against)
        print my_results

    def _comparefieldshelper(inList1, inDictio1, inList2, inDictio2):
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

    def _fieldtypedict(self, inTable):
        dictio = {}
        for fi in arcpy.ListFields(inTable):
            dictio[fi.name] = fi.type
        return dictio
            




            


        

    

























