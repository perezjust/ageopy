import os, string, sys, traceback, shutil, logging
import arcpy
arcpy.env.workspace = r"C:\\"


import expFuncs as eF
from expFuncs import *


inLine = arcpy.GetParameterAsText(0)
outPath = arcpy.GetParameterAsText(1)
coordpriority = arcpy.GetParameterAsText(4)


mei = r"C:\EXPBash"
mpm_dir = mei + "\\MilePostGen"
wkspace = mpm_dir + "\\wkspace"
measLine = wkspace + "\\measLine.shp"
inTableMP = wkspace + "\\inTableMP.txt"
inTableMPt = wkspace + "\\inTableMPt.txt"
singlePart = wkspace + "\\singlePart.shp"
inLineCopy = wkspace + "\\inLineCopy.shp"
milePosts = wkspace + "\\milePosts.shp"
milePostsT = wkspace + "\\milePostsT.shp"


def main():


    try:

        func1()

    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()



def func1():

    runChecks()

    mpmLength = prepareDataRun()

    try:

        createRouteTable(mpmLength)
        arcpy.MakeRouteEventLayer_lr(measLine, "mpmID", inTableMP, "mpmID POINT mpmLength", "lyrMilePosts", "", "", "")
        arcpy.CopyFeatures_management("lyrMilePosts", milePosts)
        arcpy.MakeRouteEventLayer_lr(measLine, "mpmID", inTableMPt, "mpmID POINT mpmLength", "lyrMilePostsT", "", "", "")
        arcpy.CopyFeatures_management("lyrMilePostsT", milePostsT)
        fieldPrecision = 5
        arcpy.AddField_management(milePosts, "MP", "Short", fieldPrecision, "")
        arcpy.AddField_management(milePostsT, "MP", "TEXT", "", "")
        arcpy.CopyFeatures_management(milePosts, outPath + "\\milePosts.shp")
        arcpy.CopyFeatures_management(milePostsT, outPath + "\\milePostsT.shp")

        calculateMP([outPath + "\\mileposts.shp", outPath + "\\milePostsT.shp"])

        arcpy.SetParameter(2, outPath + "\\milePostsT.shp")
        arcpy.SetParameter(3, outPath + "\\milePosts.shp")

    except:
        arcpy.AddMessage(traceback.format_exc())
        logging.debug(traceback.format_exc())

def calculateMP(indatalist):
    for indata in indatalist:
        ucur = arcpy.UpdateCursor(indata)
        for uc in ucur:
            newVal = float(uc.getValue("mpmLength")) / 5280
            uc.setValue("MP", newVal)
            ucur.updateRow(uc)
        del uc, ucur

def prepareDataRun():
        try:
            arcpy.CopyFeatures_management(inLine, inLineCopy)
            arcpy.AddField_management(inLineCopy, "mpmID", "TEXT", "", "")
            arcpy.CreateRoutes_lr(inLineCopy, "mpmID", measLine, "LENGTH", "", "", coordpriority, 1)
            arcpy.AddField_management(measLine, "mpmLength", "Double", "", "")
            arcpy.CalculateField_management(measLine, "mpmID", "1", "PYTHON")
            arcpy.CalculateField_management(measLine, "mpmLength", '!SHAPE.length!', "PYTHON")
            #Used a feature layer to get cursor in hopes of not locking the underlying data
            measLine1 = arcpy.MakeFeatureLayer_management(measLine)
            scurLength = arcpy.SearchCursor(measLine1)
            for scL in scurLength:
                mpmLength = scL.mpmLength
            del scurLength, scL
            r = arcpy.Delete_management(measLine1)
            return mpmLength

        except:
            arcpy.AddMessage(traceback.format_exc())
            logging.debug(traceback.format_exc())


def createRouteTable(mpmLength):
    writerMP = open(inTableMP, "w")
    writerMPt = open(inTableMPt, "w")
    writerMP.write("mpmId,mpmLength" + "\n")
    writerMP.write("1," + str(0) + "\n")
    writerMPt.write("mpmId,mpmLength" + "\n")
    writerMPt.write("1," + str(0) + "\n")
    mpmLength1 = mpmLength / 5280
    mpmLength2 = mpmLength / 528
    mile_counter = 0
    while (mpmLength1 - mile_counter) >= 1:
        mile_counter+=1
        writerMP.write("1," + str(mile_counter * 5280) + "\n")
    #writerMP.write("1," + str(int(float(mpmLength))) + "\n")
    writerMP.close()
    mile_counter2 = 0
    while (mpmLength2 - mile_counter2) >=1:
        mile_counter2+=1
        writerMPt.write("1," + str(mile_counter2 * 528) + "\n")
    writerMPt.close()


def runChecks():

    try:
        arcpy.env.overwriteOutput = True
        keepDirs = mei, mpm_dir
        for kp in keepDirs:
            if not os.path.exists(kp):
                os.mkdir(kp)
        delDirs = [wkspace]
        for dd in delDirs:
            if os.path.exists(dd):
                shutil.rmtree(dd)
            os.mkdir(dd)
        if not os.path.exists(mpm_dir + "\\log.txt"):
            logWriter = open(mpm_dir + "\\log.txt", 'w')
            logWriter.close()
            del logWriter
        logging.basicConfig(level=logging.DEBUG, filename=mpm_dir + "\\log.txt", format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        logging.debug(" ")
        logging.debug(" ")
        logging.debug("##############  New Run  ############################################")
        logging.debug("############## " + str(datetime.datetime.now()) + " ###########################")
        if arcpy.Describe(inLine).spatialReference.linearUnitName <> "Foot_US":
            arcpy.AddMessage(" ")
            arcpy.AddMessage(" ")
            arcpy.AddMessage("Input: " + inLine + " ..must be defined in feet.")
            arcpy.AddMessage(" ")
            arcpy.AddMessage(" ")
            sys.exit()
        if int(arcpy.GetCount_management(inLine).getOutput(0)) > 1:
            arcpy.AddMessage(" ")
            arcpy.AddMessage(" ")
            arcpy.AddMessage("Input: " + inLine + " ..must have only one record.")
            arcpy.AddMessage(" ")
            arcpy.AddMessage(" ")
            sys.exit()
        arcpy.MultipartToSinglepart_management(inLine, singlePart)
        if int(arcpy.GetCount_management(singlePart).getOutput(0)) > 1:
            arcpy.AddMessage(" ")
            arcpy.AddMessage(" ")
            arcpy.AddMessage("Input: " + inLine + " ..must be a non multi-part Shapefile.")
            arcpy.AddMessage(" ")
            arcpy.AddMessage(" ")
            sys.exit()
    except:
        arcpy.AddMessage(traceback.format_exc())
        logging.debug(traceback.format_exc())




if __name__ == "__main__":
    main()

