import arcpy
import traceback
import os
import sys
import datetime
import time


#Input Data Connection
input_database_connection = os.getcwd() + "\\pods_os_GISCLOUDQA.sde"

#Input sources
hcaboundary = os.path.join(input_database_connection, "PODS.GIS.HCABoundary")
dotclass = os.path.join(input_database_connection, "PODS.GIS.DOTClass")


arcpy.env.scratchWorkspace = os.getcwd()
arcpy.env.overwriteOutput = True
global_wkspace = "%scratchGDB%"#"in_memory"#




output_db_conn = os.getcwd() + "\\background_os_conn.sde"

def main():
    
    try:

        start_overlay()
        
    except:
        print traceback.format_exc()
        arcpy.AddMessage(traceback.format_exc())




class nrange(object):
    from collections import defaultdict

    def __init__(self, dictio=None):
        self.ranges = self.build_ranges(dictio)

    def build_ranges(self, dictio):
        ranges = defaultdict(list)
        for i in dictio:
            ranges[dictio["OBJECTID"]].append((dictio["BeginMeasure"], dictio["EndMeasure"]))


    def intersection(self, aRange):
        if self.upper < aRange.lower or aRange.upper < self.lower:
            return None
        else:
            return nrange(max(self.lower,aRange.lower), \
                          min(self.upper,aRange.upper))




def start_overlay():
    hcalist = build_overlay_dict(hcaboundary, "{44F65409-45E4-43A2-B705-A3176F842296}")
    #dotlist = build_overlay_dict(dotclass, "{44F65409-45E4-43A2-B705-A3176F842296}")
    print nrange(hcalist).ranges
    




def interval_intersections():
    pass




def build_overlay_dict(input_table, rid):
    dict_list = []
    sql = '"RouteEventID" = ' + "'" + rid + "'"
    with arcpy.da.SearchCursor(input_table, "*", sql) as cursor:
        for row in cursor:
            dict_list.append(dict(zip(cursor.fields, row)))
    return dict_list























def build_overlays(in_table_and_field_dict, report_name):
    print datetime.datetime.now()
    input_list = []
    for key in in_table_and_field_dict:
        input_list.append(key)

    
    layer_prep_dict = prep_overlay_inputs(input_list, in_table_and_field_dict)

    #useless step...just being lazy after refactoring
    overlay_list = []
    for j in layer_prep_dict:
        overlay_list.append(layer_prep_dict[j])
    
    overlay_table = build_overlays_iter(overlay_list, report_name)
    finalize_result_table(overlay_table)
    arcpy.CopyRows_management(overlay_table, "%scratchGDB%" + "\\" + report_name)# + ".dbf")
    
    print datetime.datetime.now()


def RETIRED_build_overlays_RETIRED(in_table_and_field_dict, report_name):
    print datetime.datetime.now()
    input_list = []
    for key in in_table_and_field_dict:
        input_list.append(key)
    join_dict = {}
    overlay_list = []#Allows me to not send the SubSystem table over to the build_overlay_iter function.  It was joined to SubSystemRange.
    layer_prep_dict = prep_overlay_inputs(input_list, in_table_and_field_dict)
    for j in layer_prep_dict:
        if os.path.basename(layer_prep_dict[j]) == "PODSGISSubSystemRange":
            join_dict["a"] = layer_prep_dict[j]
            overlay_list.append(layer_prep_dict[j])
        elif os.path.basename(layer_prep_dict[j]) == "PODSGISSubSystem":
            join_dict["b"] = layer_prep_dict[j]
        else:
            overlay_list.append(layer_prep_dict[j])
    arcpy.JoinField_management(join_dict["a"], "SubSystemEventID", join_dict["b"], "EventID", "")
    overlay_table = build_overlays_iter(overlay_list, report_name)

    arcpy.CopyRows_management(overlay_table, "%scratchGDB%" + "\\" + report_name)# + ".dbf")
    
    print datetime.datetime.now()



def build_overlays_iter(overlay_list, report_name):
    '''
        The logic for finding previous overlay result to use in next overlay result will break if
        arcpy.env.overwriteOutput is not set to True
    '''
    counter = 0
    print len(overlay_list)
    for ly in overlay_list:
        out_overlay_name = arcpy.CreateUniqueName(report_name + str(counter), global_wkspace)
        out_overlay_props = "RID" + str(counter) + " LINE From" + str(counter) +  " To" + str(counter)
        in_overlay_name = global_wkspace + "\\" + report_name + str(counter - 1)
        in_overlay_props = "RID" + str(counter - 1) + " LINE From" + str(counter - 1) +  " To" + str(counter - 1)
        common_props = "RouteEventID LINE BeginMeasure EndMeasure"
        print counter
        if counter == 0:
            #First Overlay of first two items in list
            overlay(overlay_list[0], common_props, overlay_list[1], common_props, out_overlay_name, out_overlay_props)
        elif counter == 1:
            #Second layer gets overlayed along with first layer
            pass
        elif counter == 2:
            #Third layer and second overlay
            #Has to account for the fact that the second overlay didn't happen
            if counter == len(overlay_list) - 1:
                #If last iteration and third iteration then the common_props should be the output
                in_overlay_name = global_wkspace + "\\" + report_name + str(counter - 2)
                in_overlay_props = "RID" + str(counter - 2) + " LINE From" + str(counter - 2) +  " To" + str(counter - 2)
                overlay(in_overlay_name, in_overlay_props, ly, common_props, out_overlay_name, common_props)
            else:
                in_overlay_name = global_wkspace + "\\" + report_name + str(counter - 2)
                in_overlay_props = "RID" + str(counter - 2) + " LINE From" + str(counter - 2) +  " To" + str(counter - 2)
                overlay(in_overlay_name, in_overlay_props, ly, common_props, out_overlay_name, out_overlay_props)
        elif counter == len(overlay_list) - 1:
            #Last overlay which we want to have the output properties set to BeginMeasure and EndMeasure
            overlay(in_overlay_name, in_overlay_props, ly, common_props, out_overlay_name, common_props)
        else:
            #Middle overlays
            overlay(in_overlay_name, in_overlay_props, ly, common_props, out_overlay_name, out_overlay_props)
        counter += 1
        
    return out_overlay_name

    

def overlay(in1, inprops1, in2, inprops2, out1, outprops1):
    print "=================================="
    print in1
    print inprops1
    print in2
    print inprops2
    print out1
    print outprops1
    print "=================================="
    arcpy.OverlayRouteEvents_lr(in1, inprops1, in2, inprops2, "UNION", out1, outprops1, "NO_ZERO", "FIELDS", "INDEX")




def prep_overlay_inputs(input_list, in_table_and_field_dict):
    '''
        Writing the inputs to disk in in_memory then sending the data paths over to build_overlays for
        final step actually doing the OverlayRouteEvent_lr.
    '''
    return_dict = {}
    for i in input_list:
        return_dict[i] = create_table_from_view(i, in_table_and_field_dict[i])
    return return_dict



def create_table_from_view(in_table, visible_fields_list=None):
    '''
        Use visible_fields_list to build MakeTableView_management fields parameter string.
        One of the calls to create_table_from_view doesn't need to filter fields which is why
        the second parameter for this function is optional with the None keyword.
    '''
    #table = arcpy.CreateUniqueName("".join(os.path.basename(in_table).split(".")), "%scratchGDB%")
    table = arcpy.CreateUniqueName("".join(os.path.basename(in_table).split(".")), global_wkspace)
    tableview = table + "_view"
    if visible_fields_list == None:
        visible_fields_param = ""
    else:
        visible_fields_param = build_visible_fields_param(in_table, visible_fields_list)
    arcpy.MakeTableView_management(in_table, tableview, "", "", visible_fields_param)
    arcpy.CopyRows_management(tableview, table)
    arcpy.DeleteField_management(table, "EventID")
    return table



def build_visible_fields_param(in_table, visible_fields_list):
    '''
        Builds the visible fields parameter string for MakeTableView_management.
    '''
    visible_fields_param_string = ""
    field_loader_list = []
    for i in arcpy.Describe(in_table).fields:
        field_loader = ""
        if i.name in visible_fields_list:
            field_loader = i.name + ' ' + shorten_field_name(in_table, i.name) + i.name + ' VISIBLE None'
        else:
            field_loader = i.name + ' ' + i.name + ' HIDDEN None'
        field_loader_list.append(field_loader)
    visible_fields_param_string = '"' + ";".join(field_loader_list) + '"'
    
    return visible_fields_param_string



def shorten_field_name(in_table, fieldname):
    exception_list = [
        "RouteEventID", "EventID", "SubSystemEventID", "BeginMeasure", "EndMeasure",
        "BeginMilepost", "EndMilepost", "BeginPlusFootage", "EndPlusFootage"
                    ]
    
    lookup_dict = {
        
        "PODS.GIS.CountyBoundary": "CB", "PODS.GIS.SubSystemRange": "SSR", "PODS.GIS.SubSystem": "SS",
        "PODS.GIS.OperatingPressure": "OP", "PODS.GIS.Coating": "CT", "PODS.GIS.PipeJoin": "PJ",
        "PODS.GIS.PipeSegment": "PS", "PODS.GIS.Sleeve": "SL", "PODS.GIS.TestPressure": "TP",
        "PODS.GIS.GrandfatherPressure": "GF", "PODS.GIS.DOTClass": "DC", "PODS.GIS.HCABoundary": "HB"

                }
    if fieldname in exception_list:
        return ""
    else:
        return lookup_dict[os.path.basename(in_table)] + "_"



def finalize_result_table(input_table):
    '''
        Table clean up.
    '''
##    arcpy.CalculateField_management(input_table, "BeginMilepost", "None", "PYTHON_9.3", "")
##    arcpy.CalculateField_management(input_table, "EndMilepost", "None", "PYTHON_9.3", "")
##    arcpy.CalculateField_management(input_table, "BeginPlusFootage", "None", "PYTHON_9.3", "")
##    arcpy.CalculateField_management(input_table, "EndPlusFootage", "None", "PYTHON_9.3", "")
##    arcpy.DeleteField_management(input_table, "SubSystemEventID")
    arcpy.DeleteField_management(input_table, "EventID")
    table_for_stupid_listfield = arcpy.env.scratchWorkspace + "\\scratch.gdb\\" + os.path.basename(input_table)
    print table_for_stupid_listfield
    fields = arcpy.ListFields(table_for_stupid_listfield)
    for i in fields:
        if i.aliasName == "EventID":
            arcpy.DeleteField_management(table_for_stupid_listfield, i.name)
    #flatten_table(table_for_stupid_listfield)



def dynseg_start_flag(pid, report):
    flagtable = output_db_conn + "\\background.gisprocess.DYNSEG_FLAG"
    cursor = arcpy.da.InsertCursor(flagtable, ("PID" , "STARTTIME", "STATUS", "PROCESS_NAME"))
    cursor.insertRow(pid, datetime.datetime.now(), "RUNNING", report)



def flatten_table(input_table):
    delete_list = []
    for rid in get_unique_values(input_table):
        sql = '"RouteEventID" = ' + "'" + rid + "'"
        with arcpy.da.UpdateCursor(input_table, "*", sql) as cursor:
            dup_list = compare_records(cursor, sql)
        for i in dup_list:
            delete_list.append(i)
    arcpy.AddMessage(delete_list)
        


def compare_records(cursor, sql):
    dict_list = []
    dup_list = set()
    for row in cursor:
        dict_list.append(dict(zip(cursor.fields, row)))
    for i in range(0, len(dict_list)):
        if dict_list[i]["OBJECTID"] in dup_list:
            pass
        '''
            This will only grab the ojjectid's that need to be deleted and
            not all the duplicate records.
        '''
        for x in dict_list[i+1:]:
            if is_record_duplicate(x, dict_list[i]) == "true":
                dup_list.add(x["OBJECTID"]) 
    return dup_list



##    if len(dup_list) > 0:
##        print "========================================="
##        print sql
##        print str(len(dup_list)) + " of " + str(len(dict_list))
##        arcpy.AddMessage(str(len(dup_list)) + " of " + str(len(dict_list)))
##        arcpy.AddMessage(dup_list)
##        print str(dup_list)
##        print "========================================="



def is_record_duplicate(indict1, indict2):
    checkdict = {}
    for k in indict1:
        if k == "OBJECTID":
            checkdict[k] = "dup"
        else:
            if indict1[k] == indict2[k]:
                checkdict[k] = "dup"
            else:
                checkdict[k] = "no_dup"
    switch = 0
    for i in checkdict:
        if checkdict[i] == "no_dup":
            switch = 1
    if switch == 1:
        return "false"
    else:
        return "true"



def get_unique_values(input_table):
    unique_list = set()
    with arcpy.da.SearchCursor(input_table, ["RouteEventID"]) as cursor:
            for row in cursor:
                unique_list.add(row[0])
    del cursor
    return unique_list
    
    





if __name__ == "__main__":
    main()
