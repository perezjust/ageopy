

import arcpy
import datetime


print datetime.datetime.now()

connfile = arcpy.GetParameter(0)

sdeconn = arcpy.ArcSDESQLExecute(connfile)
# storedproc = "execute dynseg.usp_ODM_REFRESH 'Agent_PKG_SPATIAL_CLASS_LOCATION_DIM_ETL'"

# storedproc1 = "SELECT DISTINCT d.sde_id, d.owner, start_time FROM sde.SDE_state_lineages a, (SELECT state_id, lineage_name FROM sde.SDE_states WHERE state_id = (SELECT state_id FROM sde.SDE_versions WHERE owner = 'SDE' AND name = 'DEFAULT')) b, sde.SDE_state_locks c, sde.SDE_process_information d WHERE a.lineage_id <= b.state_id AND a.lineage_name = b.lineage_name AND c.state_id = a.lineage_id AND c.sde_id = d.sde_id ORDER BY d.sde_id ASC;"

sp2 = "EXECUTE PODS_OMS.MAXIMOPROCESS.UPDATE_Valve_VW"

#storedproc = r"execute Python_TEST"
ret = sdeconn.execute(sp2)
if isinstance(ret, list):
    for i in ret:
        arcpy.AddMessage(i)

arcpy.AddMessage("Routine Complete")




