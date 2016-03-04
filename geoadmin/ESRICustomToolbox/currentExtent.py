import arcpy, traceback
import arcpy.mapping


## Sets the MXD file
IMXD = arcpy.mapping.MapDocument("CURRENT")
## Sets the Dataframe
DF = arcpy.mapping.ListDataFrames(IMXD, "Layers")[0]
arcpy.AddMessage(" ")
arcpy.AddMessage(" ")
arcpy.AddMessage("XMin: " + str(DF.extent.XMin) + " YMin: " + str(DF.extent.YMin) + " XMax: " + str(DF.extent.XMax) + " YMax: " + str(DF.extent.YMax))
arcpy.AddMessage(" ")
arcpy.AddMessage(" ")

