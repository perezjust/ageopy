

import arcpy
import datetime


print datetime.datetime.now()


conn = r"Database Connections\GISCloudDEV_pods_os.sde"
sdeconn = arcpy.ArcSDESQLExecute(conn)

##storedproc = "exec GIS.usp_ValidateCodedDomainOnVersion 'GIS.STATIONSERIES_VW', 'OperationalStatus', 'gnOperationalStatus', '" + '"' + "BOARDWALK\PEREZJ" + '"' + ".TEST_JPEREZ'"

##storedproc = "exec GIS.usp_ValidateCodedDomainOnVersion 'GIS.STATIONSERIES_VW', 'OperationalStatus', 'gnOperationalStatus', 'BOARDWALK\PEREZJ.TEST_JPEREZ'"

storedproc = "exec GIS.usp_ValidateCodedDomainOnVersion 'GIS.STATIONSERIES_VW', 'OperationalStatus', 'gnOperationalStatus', 'DATAQUALITY.DataQuality'"

print storedproc
ret = sdeconn.execute(storedproc)
print ret
