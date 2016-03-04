import sys
import os
import arcpy



arcpy.env.scratchWorkspace = r"O:\AppData\GIS\Cloud\Software\Boardwalk\Python\ArcToolbox\dynseg"
gdb = r"O:\AppData\GIS\Cloud\Software\Boardwalk\Python\ArcToolbox\dynseg\GISCloudDEV_background_os.sde\background.GISPROCESS.DynSeg_DOTClass"

arcpy.Append_management("%scratchGDB%" + "\\dotclass2", gdb, "NO_TEST", fieldmap)


