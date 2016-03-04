import arcpy
import traceback
import os
import sys



def main():


    try:

   
        parent_version = '"BOARDWALK\PEREZJ".DataQuality'
        target_version = arcpy.GetParameter(0)
        action = arcpy.GetParameter(1)

        arcpy.AddMessage(os.getcwd())
        arcpy.AddMessage(sys.executable)
        manager(action, parent_version, target_version)



    except:
        arcpy.AddMessage(traceback.format_exc())


def logMessage(message):
        with open(r"\\Boardwalk\Global\AppData\GIS\Cloud\Users\JPerez\log.txt", "a") as writer:
            #os.getcwd() + "\\log.txt", "a") as writer:
            writer.write("\r\n" + message)
            writer.write("\r\n" + os.getcwd())


def manager(action, parent_version, target_version):
    if action == "delete":
        delete_version(target_version)
    elif action == "create":
        create_version(parent_version, target_version)
    else:
        arcpy.AddMessage("wrong command")


def delete_version(target_version):
    dbconn = "Database Connections/GISCLOUDDEV_os_pods.sde"
    arcpy.DeleteVersion_management(dbconn, target_version)
    #logMessage(target_version)
    arcpy.AddMessage(target_version)


def create_version(parent_version, target_version):
    dbconn = "Database Connections/GISCLOUDDEV_os_pods.sde"
    arcpy.CreateVersion_management(dbconn, parent_version, target_version, "PUBLIC")
    #logMessage(parent_version)
    arcpy.AddMessage(target_version + parent_version)




if __name__ == "__main__":
    main()
