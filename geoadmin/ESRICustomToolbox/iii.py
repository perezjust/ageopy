import arcpy

for fld in arcpy.ListFields(r"Database Connections\giscloudqa_osa_pods.sde\PODS.GIS.Valve"):
    print fld.baseName + "," + fld.type + "," + fld.domain + "," + str(fld.isNullable) + "," + str(fld.required)
