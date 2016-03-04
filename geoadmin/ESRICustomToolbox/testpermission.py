
import arcpy
import sys
import traceback


def test_permission():
    path = r"O:\AppData\GIS\Cloud\SDE files\GISCloudProd PODS as OSA.sde"
    try:
        with arcpy.da.Editor(path) as editor:
            pass
        arcpy.AddMessage("Starting...")
        print "Starting..."
    except:
        arcpy.AddMessage("You do not have permission to Refresh Data.")
        print "You do not have permission to Refresh Data."
        exit()


test_permission()








