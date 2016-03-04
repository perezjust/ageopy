
import arcpy
import traceback
import os
import datetime

#temporary
arcpy.env.scratchWorkspace = r"O:\AppData\GIS\Cloud\Users\JPerez\workspace\20140514_SegmentorToolTesting_OverlayTesting"



def main():
    try:

        input_table = arcpy.GetParameter(0)

        iterate_input(input_table)#, rid_field, measure_field, milepost_field, beginplus_field, milepostboundary)

    except:
        arcpy.AddMessage(traceback.format_exc())



def iterate_input(input_table):#, rid_field, measure_field, milepost_field, beginplus_field, milepostboundary):
    cursor_field_list = [ "BeginMeasure", "EndMeasure", "BeginStation", "EndStation" ]
    with arcpy.da.SearchCursor(input_table, cursor_field_list) as cursor:
        for row in cursor:
            try:
                measdiff = row[1] - row[0]
                stationdiff = row[3] - row[2]
                #arcpy.AddMessage("Measure Diff: " + str(measdiff))
                #arcpy.AddMessage("Station Diff: " + str(stationdiff))
                arcpy.AddMessage(measdiff/stationdiff)
##                if abs(measdiff/stationdiff) < 1:
##                    arcpy.AddMessage(measdiff/stationdiff)
            except:
                pass#arcpy.AddMessage(traceback.format_exc())
            
            
    


def find_mp_plusfootage(rid, measure, milepostboundary):
    '''
        Current limitation is...
    '''
    cursor_fields = [ "BeginMeasure", "Milepost", "BeginPlusFootage",  "EndPlusFootage", "EndMeasure"]
    sql = '"RouteEventID" = ' + "'" + rid + "' and " + '"BeginMeasure" <= ' + str(measure) + ' and "EndMeasure" >= ' + str(measure)
    return_list = []
    counter = 0
    try:
        with arcpy.da.SearchCursor(milepostboundary, cursor_fields, sql) as cursor:
            for row in cursor:
                if counter == 0:
                    return_list = [rubberband_measure(measure, row[2], row[3], row[0], row[4]), row[1]]
                else:
                    pass
                counter += 1
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
