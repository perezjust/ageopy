
import arcpy
import traceback
import os
import datetime

#temporary
arcpy.env.scratchWorkspace = r"O:\AppData\GIS\Cloud\Users\JPerez\workspace\20140514_SegmentorToolTesting_OverlayTesting"



def main():
    try:

##        input_table = arcpy.GetParameter(0)
##        rid_field = arcpy.GetParameter(1)
##        measure_field = arcpy.GetParameter(2)
##        milepost_field = arcpy.GetParameter(3)
##        beginplus_field = arcpy.GetParameter(4)
##        milepostboundary = arcpy.GetParameter(5)
##
##        iterate_input(input_table, rid_field, measure_field, milepost_field, beginplus_field, milepostboundary)

    except:
        arcpy.AddMessage(traceback.format_exc())



def iterate_input(input_table, rid_field, measure_field, milepost_field, beginplus_field, milepostboundary):
    cursor_field_list = [ str(rid_field), str(measure_field), str(milepost_field), str(beginplus_field) ]
    with arcpy.da.UpdateCursor(input_table, cursor_field_list) as cursor:
        for row in cursor:
            calc_list = find_mp_plusfootage(row[0], row[1], milepostboundary)
            '''
                calc_list format [ BeginMeasure, Milepost, BeginPlusFootage ]
                or for EndMeasure it would be [ EndMeasure, Milepost, EndPlusFootage ]
            '''
            if len(calc_list) == 2:
                row[3] = calc_list[0]
                row[2] = calc_list[1]
            else:
                row[3] = 999999
                row[2] = 999999
            cursor.updateRow(row)
            
    


def find_mp_plusfootage(rid, measure, milepostboundary):
    '''
        Current limitation is...
    '''
    cursor_fields = [ "BeginMeasure", "Milepost", "BeginPlusFootage",  "EndPlusFootage", "EndMeasure"]
    sql = '"RouteEventID" = ' + "'" + rid + "' and " + '"BeginMeasure" <= ' + str(measure) + ' and "EndMeasure" >= ' + str(measure)
    return_list = []
    try:
        with arcpy.da.SearchCursor(milepostboundary, cursor_fields, sql) as cursor:
            for row in cursor:
                if counter == 0:
                    return_list = [rubberband_measure(measure, row[2], row[3], row[0], row[4]), row[1]]
                else:
                    pass
    except:
        arcpy.AddMessage(traceback.format_exc())
    return return_list



def rubberband_measure(input_measure, beg_plusfoot, end_plusfoot, beg_measure, end_measure):
    measure_range = end_measure - beg_measure
    plusfoot_range = end_plusfoot - beg_plusfoot
    conversion = plusfoot_range / measure_range
    delta_measure = abs(input_measure - beg_measure)
    return delta_measure * conversion + beg_plusfoot




if __name__ == "__main__":
    main()
