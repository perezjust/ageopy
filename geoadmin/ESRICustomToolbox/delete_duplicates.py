
import arcpy
import traceback
import os

#temporary
arcpy.env.scratchWorkspace = r"O:\AppData\GIS\Cloud\Users\JPerez\workspace\20140514_SegmentorToolTesting_OverlayTesting"
import dynseg_sharedlib as dynseg


def main():
    try:

        
        input_table = arcpy.GetParameter(0)
        #rid_field = arcpy.GetParameter(1)

        dynseg.flatten_table(input_table)#, rid_field, measure_field, milepost_field, beginplus_field, milepostboundary)

    except:
        arcpy.AddMessage(traceback.format_exc())





if __name__ == "__main__":
    main()
