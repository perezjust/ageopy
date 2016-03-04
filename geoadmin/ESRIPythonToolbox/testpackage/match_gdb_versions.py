import arcpy
import traceback
import os
import sys
import getpass
import shutil

arcpy.env.overwriteOutput = True



def main():
    print "hi"
    #debug!!!
    pytmain("fakeparams")


def pytmain(params):
    try:
        
        dbconn = manage_runtime_params(params[0])
        
        check_version_parent(dbconn)
        
    except:
        arcmessage(traceback.format_exc())



def child_versions(dbconn):
    arcpy.env.workspace = dbconn
    for i in arcpy.da.ListVersions():
        #arcmessage(i.name)
        if str(i.name) != "sde.DEFAULT":
            #arcmessage(str(i.name))
            if str(i.name) != "DATAQUALITY.DataQuality":
                arcmessage(str(i.name))


def check_version_parent(dbconn):
    arcpy.env.workspace = dbconn
    for i in arcpy.da.ListVersions():
        #arcmessage(i.name)
        if str(i.parentVersionName) == "sde.DEFAULT":
            #arcmessage(str(i.name))
            if str(i.name) != "DATAQUALITY.DataQuality":
                arcmessage(str(i.name))


def manage_runtime_params(param1):
    if get_arcpy_runtime() == "python":
        returnparam1 = r"Database Connections\GISCLOUDDEV_os_pods.sde"
    elif get_arcpy_runtime() == "arcmap":
        returnparam1 = param1.valueAsText
    return returnparam1


def arcmessage(message):
    print message
    arcpy.AddMessage(message)


def get_arcpy_runtime():
    if str(sys.executable).endswith("ArcMap.exe"):
        executable = "arcmap"
    elif str(sys.executable).endswith("pythonw.exe"):
        executable = "python"
    return executable


def set_mxd():
    if get_arcpy_runtime() == "python":
        mxdpath = r"O:\AppData\GIS\Cloud\Users\JPerez\workspace\20141118_DataRefreshTesting\PODS_EventTables_For_Maximo.mxd"
        mxd = arcpy.mapping.MapDocument(mxdpath)
    elif get_arcpy_runtime() == "arcmap":
        mxd = arcpy.mapping.MapDocument("CURRENT")
    return mxd


    





if __name__ == "__main__":
    main()
