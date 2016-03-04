import os
import string
import sys
import shutil
import logging
import datetime
import traceback




class logger:

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


def callerfile( back = 0 ):
   return sys._getframe( back + 1 ).f_code.co_filename

def callerline( back = 0 ):
    return sys._getframe( back + 1 ).f_lineno

def callerfunction( back = 0):
    return sys._getframe( back + 1 ).f_code.co_name

def callerwhere( back = 0 ):
   frame = sys._getframe( back + 1 )
   return "%s/%s %s()" % ( os.path.basename( frame.f_code.co_filename ), 
                           frame.f_lineno, frame.f_code.co_name )







