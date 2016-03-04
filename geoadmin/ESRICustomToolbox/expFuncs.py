import os, string, sys, shutil, logging, datetime, traceback, arcpy

class meiSetUp:

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


class logIt:

    def __init__(self, arg1, arg2=None):
        self.log = arg1
        self.discrete = arg2
        dtn = str(datetime.datetime.now()).split(" ")
        dayValue = "".join(dtn[0].split("-"))
        dayValueAlt = dayValue + "_" + "".join(str("".join(dtn[1].split(":"))).split("."))
        if self.discrete == None or self.discrete == "False":
            self.fileLogPath = self.log + "\\" + "log_python.txt"
        else:
            self.fileLogPath = self.log + "\\" + "log_python" + dayValueAlt + ".txt"
        if not os.path.exists(self.log):
            os.mkdir(self.log)
        makeFile(self.fileLogPath)
        logIt.logSetUp(self)

    def logSetUp(self):
        logging.basicConfig(level=logging.DEBUG, filename=self.fileLogPath,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
    def logFilePath(self):
        return self.fileLogPath

    def logTrace(self, arg1):
        #logIt.logSetUp(self)
        logging.debug(traceback.format_exc() + " - " + arg1 )
        arcMessage(arg1 + "\n" + traceback.format_exc())

    def logMessageHeader(self, arg1):
        logging.debug(" ")
        logging.debug("=================================================")
        logging.debug(arg1)
        logging.debug("=================================================")

    def logMessage(self, arg1):
        logging.debug(arg1)


##class FeatureLayer:
##
##    def __init__(self, arg1, sql=None, cursorType=None, field=None):
##        self.arg1 = arg1
##        self.sql = sql
##        self.cT = cursorType
##        self.fld = field
##        self.unqList = []
##        self.cursorObject = []
##        #Start
##        FeatureLayer.returnFL(self, self.arg1, self.sql)
##
##    def returnFL(self, feat, sql):
##        arcpy.MakeFeatureLayer_management(feat, feat + "_fl", sql)
##        fl_count = int(arcpy.GetCount_management(feat + "_fl").getOutput(0))
##        if fl_count > 0:
##            if self.cT is not None:
##                FeatureLayer.SearchCurs(self, feat + "_fl", self.cT, self.fld )
##            return feat + "_fl"
##        else:
##            logIt.logTrace(logIt, self.arg1 + " did not return any features")
##    #@staticmethod
##    def SearchCurs(self, arg1, cursorType, field):
##        if cursorType == "search":
##            self.cursorObject = arcpy.SearchCursor(arg1)
##            for row in self.cursorObject:
##                if row not in self.unqList:
##                    self.unqList.append(row.getValue(field))
##        else:
##            logIt.logTrace(self, "Wrong parameter given for cursorType")
##        return self.unqList


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

def getNiceDate():
    dtn = str(datetime.datetime.now()).split(" ")
    dayValue = "".join(dtn[0].split("-"))
    dayValueAlt = dayValue + "_" + "".join(str("".join(dtn[1].split(":"))).split("."))
    return dayValue





