import webbrowser
import arcpy
import traceback
import os




def main():
    try:

##        path = r"O:\AppData\GIS\Cloud\Imagery\GS_2013"
##        arcpy.env.workspace = path
##        for i in arcpy.ListRasters("*", "All"):
##            print arcpy.Raster(i).catalogPath
##            print 25 * "-"

        rastpath = r"O:\AppData\GIS\Cloud\Imagery\GS_2013\Steve_Copeland_1.sid"
        rast = arcpy.Raster(rastpath)
        print rast.pixelType
##        for i in dir(rast):
##            rast
##            print i

    except:
        arcpy.AddMessage(traceback.format_exc())





if __name__ == "__main__":
    main()
