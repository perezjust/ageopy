import arcpy


for i in arcpy.da.ListDomains(r"\\aws0isqv1\c$\geoproc\GISCloudDev_pods_os.sde"):
    print i.name
