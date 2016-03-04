
import os, string, sys, traceback
import arcpy




allfiles = []
m = arcpy.GetParameterAsText(0)
n = arcpy.GetParameterAsText(1)
shapeType = arcpy.GetParameterAsText(2)

arcpy.env.Workspace = n
arcpy.OverWriteOutput = True

try:
        for root,dir,files in os.walk(m):
                filelist = [ os.path.join(root,fi) for fi in files if fi.endswith(".shp")]
                for f in filelist:
                        allfiles.append(f)
        arcpy.AddMessage("There are " + str(len(allfiles)) + " files to be processed.")
        arcpy.AddMessage("These files did not get copied over:")
        proclength = len(allfiles)
        for i in allfiles:
                try:
                        if proclength == int((len(allfiles) * .75)):
                            arcpy.AddMessage("~25% complete")
                        if proclength == int((len(allfiles) * .5)):
                            arcpy.AddMessage("~50% complete")
                        if proclength == int((len(allfiles) * .25)):
                            arcpy.AddMessage("~75% complete")
                        dsc = arcpy.Describe(i)
                        validName = arcpy.ValidateTableName(os.path.basename(i)[:-4] + "_" + os.path.dirname(i).split("\\")[-1], n)
                        name = arcpy.CreateUniqueName(validName, n)
                        if shapeType != "":
                                if dsc.shapetype == shapeType:
                                        arcpy.CopyFeatures_management(i, name)
                        else:
                                arcpy.CopyFeatures_management(i, name)
                        proclength -= 1
                except:
                        arcpy.AddMessage(traceback.format_exc())
                        arcpy.AddMessage(i)

except:
        arcpy.AddMessage(traceback.format_exc())

