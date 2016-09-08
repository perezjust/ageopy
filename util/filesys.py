import os
import string
import sys
import shutil
import logging
import datetime
import traceback
from collections import defaultdict




class AGEOSetUp(object):

    def __init__(self, arg1):
        self.mei_path = r"C:\EXPBash"
        self.top_path = self.mei_path + "\\" + arg1
        self.log_path = self.top_path + "\\log"
        self.workspace_path = self.top_path + "\\wkspace"
        meiSetUp.keepDirs(self)



    def keepDirs(self):
        makeDirs = [self.mei_path, self.top_path, self.log_path, self.workspace_path]
        for md in makeDirs:
            if not os.path.exists(md):
                os.mkdir(md)


    def refreshDirs(self, arg1=list):
        #To refresh directories for new gp run
        #call meiSetUp.refreshDirs(listOfDirectories)
        for lr in arg1:
            if os.path.exists(self.workspace_path + "\\" + lr):
                shutil.rmtree(self.workspace_path + "\\" + lr)
            os.mkdir(self.workspace_path + "\\" + lr)
        if len(arg1) == 1:
            return str(self.workspace_path + "\\" + lr)

    def display(self):
        mess = meiSetUp.logSetUp(self)
        arcMessage(mess)



def manage_runtime_params(param1):
    """
        How do we find if our parameters are coming from arcmap
    """
    if get_arcpy_runtime() == "python":
        returnparam1 = r"Database Connections\GISCloudPROD_pods_os.sde"
    elif get_arcpy_runtime() == "arcmap":
        returnparam1 = param1.valueAsText
    return returnparam1


def get_calling_app():
    if str(sys.executable).endswith("ArcMap.exe"):
        executable = "arcmap"
    elif str(sys.executable).endswith("pythonw.exe"):
        executable = "python"
    return executable



def build_walk_list(target_dir, search_filter):
    allfiles = []
 
    for root,dir,files in os.walk(target_dir):
                filelist = [ os.path.join(root,fi) for fi in files if fi.endswith(search_filter)]
                for f in filelist:
                        allfiles.append(f)
    return allfiles



def makeFile(arg1):
    if not os.path.exists(arg1):
        logWriter = open(arg1, 'w')
        logWriter.close()
        del logWriter
        return arg1



def arcMessage(arg1):
    arcpy.AddMessage(" ")
    arcpy.AddMessage(arg1)
    arcpy.AddMessage(" ")



def makeQueryListUnique(lyr,field):
    if len(arcpy.ListFields(lyr, field)) == 0:
        arcMessage("No field called: " + field + ".  function makeQueryListUnique is breaking.")
        sys.exit()
    queryList=[]
    scur=arcpy.SearchCursor(lyr)
    for row in scur:
        val = row.getValue(field)
        if val not in queryList:
            queryList.append(val)
    return queryList



def findDuplicateValue(lyr,field):
    if len(arcpy.ListFields(lyr, field)) == 0:
        arcMessage("No field called: " + field + ".  function makeQueryListUnique is breaking.")
        sys.exit()
    queryList=[]
    queryListDup=[]
    scur=arcpy.SearchCursor(lyr)
    for row in scur:
        val = row.getValue(field)
        if val in queryList:
            queryListDup.append(val)
        else:
            queryList.append(val)
    return queryListDup



def loadFeatureSet(inShape):
    featSet = arcpy.FeatureSet()
    featSet.load(inShape)
    return featSet



def checkForField(inTable, fieldName):
    fieldPresence = 0
    flds = arcpy.Describe(inTable).fields
    for fld in flds:
        if fld.name == fieldName:
            fieldPresence = 1
    return fieldPresence



def get_nice_date(alt=None):
    dtn = str(datetime.datetime.now()).split(" ")
    dayValue = "".join(dtn[0].split("-"))
    dayValueAlt = dayValue + "_" + "".join(str("".join(dtn[1].split(":"))).split("."))
    if alt == None:
        return dayValue
    else:
        return dayValueAlt



def finder(filelist, search):
    print "kpft rocks!"
    mydict = defaultdict(list)
    for i in filelist:
        with open(i,'r') as f:
            for line in f:
                if line.find(search) <> -1:
                #output = f.read()
                #if output.find(search) <> -1:
                    mydict[i] = line
    return mydict






