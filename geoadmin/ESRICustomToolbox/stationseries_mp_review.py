import arcpy
import traceback
import os
import sys
import datetime
import time



arcpy.env.scratchWorkspace = os.getcwd()
arcpy.env.overwriteOutput = True
global_wkspace = "%scratchGDB%"#"in_memory"#




output_db_conn = os.getcwd() + "\\background_os_conn.sde"

def main():
    
    try:
        
        input_database_connection = os.getcwd() + "\\pods_os_GISCLOUDQA.sde"
        stationseries = os.path.join(input_database_connection, r"PODS.GIS.Transmission\PODS.GIS.StationSeries")
        milepost = os.path.join(input_database_connection, "PODS.GIS.MilepostBoundary")
        lineloop = os.path.join(input_database_connection, "PODS.GIS.LineLoop")
        
        iterate_ss(stationseries, milepost)
        
        
    except:
        print traceback.format_exc()

    



def iterate_ss(input_table, milepost):
    print "ID, SS Measure, MP Measure, Measure Diff, MP Found, Geometric Length, Geometry Diff"
    #ss_dict = build_ss_cont_dict(input_table)
    #mp_dict = build_milepost_dict(milepost)



    ss_dict = ({u'{CA81BF5A-1E12-42AF-9B60-583BD4A3903C}': [(u'{CA81BF5A-1E12-42AF-9B60-583BD4A3903C}', 293725.0, 293862.8362256514)]})
    mp_dict = {u'{CA81BF5A-1E12-42AF-9B60-583BD4A3903C}': 810.0}


    
    for eventid in ss_dict:
        if eventid in mp_dict.keys():
            print str(eventid) + ", " +  str(ss_dict[eventid][0][1]) + " , " + str(mp_dict[eventid]) + ", " + str(ss_dict[eventid][0][1] - mp_dict[eventid]) + ", Yes" + ", " + str(ss_dict[eventid][0][2]) + ", " + str(ss_dict[eventid][0][1] - ss_dict[eventid][0][2])
        else:
            print str(eventid) + ", " + str(ss_dict[eventid][0][1]) + ", 0, 0, No"



def build_ss_cont_dict(input_table):
    from collections import defaultdict
    eventid_list = defaultdict(list)
    sql = '"RefMode" = ' + "'" + "Continuous" + "'"
    with arcpy.da.SearchCursor(input_table, ["EventID", "LineLoopEventID", "BeginMeasure", "EndMeasure", "SHAPE@"], sql) as cursor:
            for row in cursor:
                eventid_list[row[0]].append((row[1], row[3] - row[2], row[4].getLength("GEODESIC") * 3.28084))
                print eventid_list
    del cursor
    return eventid_list



def build_ss_eng_dict(stationseries, eventid_list):
    #sorted_dict = sorted(mvalues.iteritems(), key=lambda (k,v): v[0], reverse=False)
    meas_dict = {}
    rid_list = get_unique_values(stationseries, "RouteEventID")
    for rid in rid_list:
        sql = '"RouteEventID" = ' + "'" + rid + "'"
        meas_list = []
        with arcpy.da.SearchCursor(stationseries, ["BeginMeasure", "EndMeasure"], sql) as cursor:
                for row in cursor:
                    meas_list.append(row[1] - row[0])
        meas_dict[rid] = sum(meas_list)
    return meas_dict



def build_milepost_dict(milepost):
    meas_dict = {}
    rid_list = get_unique_values(milepost, "RouteEventID")
    for rid in rid_list:
        sql = '"RouteEventID" = ' + "'" + rid + "'"
        meas_list = []
        with arcpy.da.SearchCursor(milepost, ["BeginMeasure", "EndMeasure"], sql) as cursor:
                for row in cursor:
                    meas_list.append(row[1] - row[0])
        meas_dict[rid] = sum(meas_list)
        print meas_dict
    return meas_dict



def get_unique_values(input_table, field):
    unique_list = set()
    with arcpy.da.SearchCursor(input_table, [field]) as cursor:
            for row in cursor:
                unique_list.add(row[0])
    del cursor
    return unique_list



if __name__ == "__main__":
    main()
