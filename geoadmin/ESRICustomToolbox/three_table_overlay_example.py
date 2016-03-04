
import arcpy
import traceback
import os

#temporary
arcpy.env.scratchWorkspace = r"O:\AppData\GIS\Cloud\Users\JPerez\workspace\20140514_SegmentorToolTesting_OverlayTesting"


#Load required toolboxes
#arcpy.ImportToolbox("C:/APPS/Python27/ArcGIS10.1/Lib/site-packages/boardwalk/esri/toolboxes/boardwalk.pyt")


def main():
    try:

        #Output source
        output_database_connection = r"Database Connections\GISCloudQA_os_background.sde"
        dotclass_output_result = os.path.join(output_database_connection, "background.GISPROCESS.DOTClass_DynSeg")

        #Input sources
        input_database_connection = r"Database Connections\GISCLOUDPROD_os_pods.sde"
        dotclass = os.path.join(input_database_connection, "PODS.GIS.DOTClass")
        countyboundary = os.path.join(input_database_connection, "PODS.GIS.CountyBoundary")
        subsystemrange = os.path.join(input_database_connection, "PODS.GIS.SubSystemRange")
        subsystem = os.path.join(input_database_connection, "PODS.GIS.SubSystem")
        stationseries = os.path.join(input_database_connection, r"PODS.GIS.Transmission\PODS.GIS.StationSeries")
        milepostboundary = os.path.join(input_database_connection, "PODS.GIS.MilepostBoundary")

        #Configuring which fields to be carried to final table via the MakeTableView_management call.
        dotclass_visible_fields = "OBJECTID, SourceCL, Description, Comments, RouteEventID, BeginMeasure, EndMeasure, BeginMilepost, EndMilepost, BeginPlusFootage, EndPlusFootage, RatingCL, DesignCL, MethodCL, PreviousClassRatingCL"
        countyboundary_visible_fields = "OBJECTID, Description, RouteEventID, BeginMeasure, EndMeasure, StateCL"
        subsystemrange_visible_fields = "OBJECTID, RouteEventID, BeginMeasure, EndMeasure, SubSystemEventID"
        subsystem_visible_fields = "OBJECTID, EventID, SubSystemName"

        #Mapping datasource to fields wanted. To be used as a parameter.
        in_table_and_field_dict = {dotclass: dotclass_visible_fields, countyboundary: countyboundary_visible_fields, subsystemrange: subsystemrange_visible_fields, subsystem: subsystem_visible_fields}

        #Start
        overlay_input_dict = prep_overlay_inputs(dotclass, countyboundary, subsystemrange, subsystem, in_table_and_field_dict)
        build_overlays(overlay_input_dict, stationseries, milepostboundary)

    except:
        arcpy.AddMessage(traceback.format_exc())



def issue_sql_statement():
    sdeconn = arcpy.ArcSDESQLExecute(r"Database Connections\GISCloudQA_os_background.sde")
            


def create_table_from_view(in_table, visible_fields_list=None):
    '''
        Use visible_fields_list to build MakeTableView_management fields parameter string.
        One of the calls to create_table_from_view doesn't need to filter fields which is why
        the second parameter for this function is optional with the None keyword.
    '''
    table = arcpy.CreateUniqueName("".join(os.path.basename(in_table).split(".")), "%scratchGDB%")
    tableview = table + "_view"
    if visible_fields_list == None:
        visible_fields_param = ""
    else:
        visible_fields_param = build_visible_fields_param(in_table, visible_fields_list)
    arcpy.MakeTableView_management(in_table, tableview, "", "", visible_fields_param)
    arcpy.CopyRows_management(tableview, table)
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
            field_loader = i.name + ' ' + i.name + ' VISIBLE None'
        else:
            field_loader = i.name + ' ' + i.name + ' HIDDEN None'
        field_loader_list.append(field_loader)
    visible_fields_param_string = '"' + ";".join(field_loader_list) + '"'
    return visible_fields_param_string


def prep_overlay_inputs(dotclass, countyboundary, subsystemrange, subsystem, in_table_and_field_dict):
    '''
        Writing the inputs to disk in %scratchGDB% then sending the data paths over to build_overlays for
        final step actually doing the OverlayRouteEvent_lr.
    '''
    dotclassview = create_table_from_view(dotclass, in_table_and_field_dict[dotclass])
    countyboundaryview = create_table_from_view(countyboundary, in_table_and_field_dict[countyboundary])
    subsystemrangeview = create_table_from_view(subsystemrange, in_table_and_field_dict[subsystemrange])
    subsystemview = create_table_from_view(subsystem, in_table_and_field_dict[subsystem])
    return { "dotclass": dotclassview, "county": countyboundaryview, "subsysrange": subsystemrangeview, "subsys": subsystemview }


def build_overlays(overlay_input_dict, stationseries, milepostboundary):
    '''
        The overlay_input_dict dictionary is using dictionary keys hard coded in the
        return statement of the prep_overlay_inputs function. The keys are mapped to the
        OverlayRouteEvents_lr inputs which are in the %scratchGDB%.
        
    '''
    arcpy.JoinField_management(overlay_input_dict["subsysrange"], "SubSystemEventID", overlay_input_dict["subsys"], "EventID", "")
    subsysrange_jointable = arcpy.CreateUniqueName("".join(os.path.basename(overlay_input_dict["subsysrange"]).split(".")) + "_join", "%scratchGDB%")
    arcpy.CopyRows_management(overlay_input_dict["subsysrange"], subsysrange_jointable)
    first_overlay_table = arcpy.CreateUniqueName("first_overlay", "%scratchGDB%")
    arcpy.OverlayRouteEvents_lr(overlay_input_dict["dotclass"], "RouteEventID LINE BeginMeasure EndMeasure", overlay_input_dict["county"], "RouteEventID LINE BeginMeasure EndMeasure", "UNION", first_overlay_table, "NewRID LINE NewFrom NewTo", "NO_ZERO", "FIELDS", "INDEX")
    second_overlay_table = arcpy.CreateUniqueName("second_overlay", "%scratchGDB%")
    arcpy.OverlayRouteEvents_lr(first_overlay_table, "NewRID LINE NewFrom NewTo", subsysrange_jointable, "RouteEventID LINE BeginMeasure EndMeasure", "UNION", second_overlay_table, "RouteEventID LINE BeginMeasure EndMeasure", "NO_ZERO", "FIELDS", "INDEX")
    finalize_result_table(second_overlay_table, stationseries, milepostboundary)


def finalize_result_table(input_table, stationseries, milepostboundary):
    '''
        Table clean up.
    '''
    arcpy.CalculateField_management(input_table, "BeginMilepost", "None", "PYTHON_9.3", "")
    arcpy.CalculateField_management(input_table, "EndMilepost", "None", "PYTHON_9.3", "")
    arcpy.CalculateField_management(input_table, "BeginPlusFootage", "None", "PYTHON_9.3", "")
    arcpy.CalculateField_management(input_table, "EndPlusFootage", "None", "PYTHON_9.3", "")
    arcpy.DeleteField_management(input_table, "SubSystemEventID")
    arcpy.DeleteField_management(input_table, "EventID")
    for i in arcpy.Describe(input_table).fields:
        if i.aliasName == "EventID":
            arcpy.DeleteField_management(input_table, i.name)
    #arcpy.CalculateMilepostPlusFootageFromMeasure_boardwalk(input_table, "RouteEventID", "UPPER", "EndMeasure", "EndMilepost", "EndPlusFootage", milepostboundary, stationseries)
    #arcpy.CalculateMilepostPlusFootageFromMeasure_boardwalk(input_table, "RouteEventID", "UPPER", "BeginMeasure", "BeginMilepost", "BeginPlusFootage", milepostboundary, stationseries)

    




if __name__ == "__main__":
    main()
