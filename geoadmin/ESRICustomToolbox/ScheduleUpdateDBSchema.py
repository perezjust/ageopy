import arcpy
import os, string, sys, traceback
from os.path import join


import expFuncs as expF
from expFuncs import *
import gpFuncs as gpF
from gpFuncs import *




def main():

        exp = meiSetUp("updateDBSchema")
        log = logIt(exp.logPath)
        in_features = arcpy.GetParameter(0)
        
        try:
                writeConfig(exp, in_features)
                
        except:
                log.logTrace(traceback.format_exc())





def writeConfig(exp, in_features):
        delete_file = exp.wkspacePath + "\\" + "deletes.txt"
        if os.path.exists(delete_file):
                os.remove(delete_file)
        expF.makeFile(delete_file)
        writer = open(delete_file, "w")
        writerList = []
        for i in in_features:
                writerList.append(str(i))
        writer.write(",".join(writerList))
        writer.close()
        
        
     
     
        




if __name__ == "__main__":
    main()


