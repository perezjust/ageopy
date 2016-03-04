import os
import string
import sys
import traceback
import shutil
import logging
import os.path
import time
import arcpy
import arceditor



def main():


    try:
        
        mxd = r"O:\AppData\GIS\Cloud\Users\JPerez\workspace\20140716_ViewTest\ViewTest.mxd"
        get_layers(mxd)

    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()



def get_layers(mxd):
    input_list = []
    mxd = arcpy.mapping.MapDocument(mxd)
    #arcpy.AddMessage(mxd.activeDataFrame)
    df = arcpy.mapping.ListDataFrames(mxd, mxd.activeDataFrame.name)[0]
    for i in arcpy.mapping.ListTableViews(mxd):
        input_list.append(i)
    print input_list



if __name__ == "__main__":
    main()





