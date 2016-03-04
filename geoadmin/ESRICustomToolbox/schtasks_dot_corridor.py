import os
import string
import sys
import traceback
import shutil
import logging
import os.path
import time
import arcpy



def main():


    try:

        mxd_folder = "\\aws0fspv1.boardwalk.corp\Shared$\AppData\GIS\Cloud\Users\JPerez\workspace\20150403_DOTCorridor"
        for mxd in os.listdir(mxd_folder):
            print mxd
##            if mxd.endswith("mxd"):
##                print mxd

    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()



def get_layers(mxd):
    input_list = []
    mxd = arcpy.mapping.MapDocument(mxd)
    df = arcpy.mapping.ListDataFrames(mxd, mxd.activeDataFrame.name)[0]
    for i in arcpy.mapping.ListTableViews(mxd):
        input_list.append(i.dataSource.split("\\")[-1])
    return input_list



if __name__ == "__main__":
    main()





