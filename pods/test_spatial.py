import arcpy
import os
import sys
import spatial


path1 = r"O:\AppData\GIS\Cloud\SDE files\GISCloudDev PODS.sde\PODS.GIS.Transmission\PODS.GIS.StationSeries"
path = r"O:\AppData\GIS\Cloud\SDE files\GISCloudDev PODS.sde\PODS.GIS.DOTClass"
podsitem = spatial.PODSEventTable(path).validate_measures()


##sys.path.append(r"O:\AppData\GIS\Cloud\Users\JPerez\gh\ageopy\esri")
##import esri.dataelement as de
##
##de.GDBElement(path1)




