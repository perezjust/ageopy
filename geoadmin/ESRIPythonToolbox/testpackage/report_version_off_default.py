import arcpy
import traceback
import os
import sys
import getpass
import shutil

arcpy.env.overwriteOutput = True



def main():
    print "Main is entry point on this run!"
    #debug!!!
    pytmain("fakeparams")


def pytmain(params):
    try:
        
        dbconn = manage_runtime_params(params[0])
        check_version_parent(dbconn)
        
    except:
        arcmessage(traceback.format_exc())


def check_version_parent(dbconn):
    arcpy.env.workspace = dbconn
    return_list = []
    for i in arcpy.da.ListVersions():
        if str(i.parentVersionName) == "sde.DEFAULT":
            if str(i.name) != "DATAQUALITY.DataQuality":
                return_list.append(str(i.name))
    if len(return_list) > 0:
        for x in return_list:
            arcmessage(x)
    else:
        arcmessage("There are None")


def manage_runtime_params(param1):
    if get_arcpy_runtime() == "python":
        returnparam1 = r"Database Connections\GISCloudDev_pods_os.sde"
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
