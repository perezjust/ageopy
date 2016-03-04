
import arcpy
import traceback
import os

#temporary
arcpy.env.scratchWorkspace = r"O:\AppData\GIS\Cloud\Users\JPerez\workspace\20140514_SegmentorToolTesting_OverlayTesting"



def main():
    try:



    except:
        arcpy.AddMessage(traceback.format_exc())



def iterate_input(input_table, rid_field, measure_field, milepost_field, beginplus_field, milepostboundary):
    cursor_list = [ str(rid_field), str(measure_field), str(milepost_field), str(beginplus_field) ]
    with arcpy.da.UpdateCursor(input_table, cursor_list) as cursor:
        for row in cursor:
            calc_list = find_mp_plusfootage(row[0], row[1], milepostboundary)
            '''
                calc_list format [ BeginMeasure, Milepost, BeginPlusFootage ]
            '''
            #arcpy.AddMessage(str(calc_list) + str(len(calc_list)))
            if len(calc_list) == 3:
                row[3] = abs(row[1] - calc_list[0]) + calc_list[2]
                row[2] = calc_list[1]
            elif len(calc_list) == 0:
                row[3] = 999999
                row[2] = 999999
            cursor.updateRow(row)



def rubberband_measure():
    pass
            


def find_mp_plusfootage(rid, measure, milepostboundary):
    '''
        Current limitation is...
        
    '''
    cursor_fields = [ "BeginMeasure", "Milepost", "BeginPlusFootage",  ]
    sql = '"RouteEventID" = ' + "'" + rid + "' and " + '"BeginMeasure" <= ' + str(measure) + ' and "EndMeasure" >= ' + str(measure)
    counter = 0
    return_list = []
    
    try:
        with arcpy.da.SearchCursor(milepostboundary, cursor_fields, sql) as cursor:
            for row in cursor:
                counter += 1
                return_list = [ row[0], row[1], row[2] ]
                '''
                    calc_list format for the return should be [ BeginMeasure, Milepost, BeginStation ]
                '''
    except:
        arcpy.AddMessage(traceback.format_exc())



        

    if len(return_list) != 3:
        '''
            Checking that at least one record was found
        '''
        arcpy.AddMessage("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        arcpy.AddMessage("This measure " + str(measure) + " for RID: " + rid + " has no corresponding data in the Milepost Boundary table.")
        arcpy.AddMessage(sql)
        return_list = []
        arcpy.AddMessage(return_list)
        return []
    elif counter != 1:
        '''
            Checking that milepost boundary query returned only one result
        '''
        arcpy.AddMessage("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        arcpy.AddMessage("This measure " + str(measure) + " for RID: " + rid + " does not have only one record in the Milepost Boundary table.")
        arcpy.AddMessage(sql)
        return_list = []
        arcpy.AddMessage(return_list)
        return []
    return return_list




if __name__ == "__main__":
    main()
