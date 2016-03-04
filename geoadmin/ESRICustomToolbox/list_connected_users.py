import webbrowser
import arcpy
import traceback
import os




def main():
    try:

##        path = r"O:\AppData\GIS\Cloud\SDE files"
##        for i in os.listdir(path):
##            if i.endswith(".sde"):
##                print "*" * 45
##                print i
##                for j in arcpy.ListUsers(os.path.join(path, i)):
##                    print j
        sdeconn = r"Database Connections\AWS0SQQV1_SDE_PODS.sde"
        for j in arcpy.ListUsers(sdeconn):
                    print j

    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()





if __name__ == "__main__":
    main()
