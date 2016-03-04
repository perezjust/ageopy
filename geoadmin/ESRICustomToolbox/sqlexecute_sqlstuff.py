import arcpy
import datetime


print datetime.datetime.now()

connfile = r"O:\AppData\GIS\Cloud\SDE files\GISCloudDev PODS.sde"

sdeconn = arcpy.ArcSDESQLExecute(connfile)

sp2 = "SELECT * FROM GIS.STATIONSERIES"

ret = sdeconn.execute(sp2)
if isinstance(ret, list):
    for i in ret:
        arcpy.AddMessage(i)

arcpy.AddMessage("Routine Complete")
