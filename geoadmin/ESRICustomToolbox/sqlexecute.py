

import arcpy
import datetime


print datetime.datetime.now()

#conn = r"O:\AppData\GIS\Cloud\SDE files\GISCloudDev PODS.sde"
conn = r"Database Connections\GISCloudQA_pods_os.sde"
sdeconn = arcpy.ArcSDESQLExecute(conn)
##storedproc = "execute dynseg.usp_ODM_REFRESH 'Agent_PKG_SPATIAL_CLASS_LOCATION_DIM_ETL'"
##
storedproc1 = "SELECT DISTINCT d.sde_id, d.owner, start_time FROM sde.SDE_state_lineages a, (SELECT state_id, lineage_name FROM sde.SDE_states WHERE state_id = (SELECT state_id FROM sde.SDE_versions WHERE owner = 'SDE' AND name = 'DEFAULT')) b, sde.SDE_state_locks c, sde.SDE_process_information d WHERE a.lineage_id <= b.state_id AND a.lineage_name = b.lineage_name AND c.state_id = a.lineage_id AND c.sde_id = d.sde_id ORDER BY d.sde_id ASC;"

#storedproc = r"execute Python_TEST"
storedproc2 = "SELECT * FROM GIS.HOP"

ret = sdeconn.execute(storedproc2)
#print type(ret)
print ret


##flds = [ "RID", "BeginMeasure" ]
##sql_list = []
##for i in arcpy.da.SearchCursor(r"\\aws0tspv30\c$\geoproc\GISCloudDEV_background_gisprocess.sde\background.GISPROCESS.DYNSEG_PHMSA", flds):
##    sqlpart2 = " and BeginMeasure <= " + str(i[1]) + " and EndMeasure >= " + str(i[1])
##    sqlpart1 = "select BeginMeasure, MilePost, BeginPlusFootage, EndPlusFootage, EndMeasure from PODS.GIS.MilepostBoundary where RouteEventID = '" + i[0] + "'" 
##    sql = sqlpart1 + sqlpart2
##    sql_list.append(sql)
##    #sql = '"RouteEventID" = ' + "'" + rid + "' and " + '"BeginMeasure" <= ' + str(measure) + ' and "EndMeasure" >= ' + str(measure)
##    #ret = sdeconn.execute(sql)
##
##print datetime.datetime.now()
