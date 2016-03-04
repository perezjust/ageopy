import arcpy
import traceback
import os
import sys
import datetime
import time
import getpass
import json
import imp


arcpy.env.overwriteOutput = True




def main():#(report_name, main_config_path, parent_path, environment, execute_sp_flag):
    event_tables = arcpy.GetParameter(0)
    arcpy.AddMessage(event_tables)
    
    try:

        build_overlays(event_tables)
        
    except:
        print traceback.format_exc()
        arcpy.AddMessage(traceback.format_exc())
        #log.logMessage(traceback.format_exc())
    


def build_overlays(in_table_list):
    #test_permission()
    for table in in_table_list:
        sanitize_fields(table)
    #overlay_table = build_overlays_iter(in_table_list)
    

def assign_output(report_name, main_config, report_config, parent_path, environment):
    path = parent_path + "\\" + environment + "\\" + main_config["DATABASECONNECTIONFOLDER"]
    outputdb = os.path.join(path, environment + "_" + main_config["DYNSEGSDE"])
    rootname = outputdb + "\\background.DynSeg."
    return rootname + report_config[report_name]["OUTPUTNAME"]


def qualify_field_name(in_table, main_config):
        for item in main_config:
            if os.path.basename(in_table) in main_config[item]:
                return main_config[item][1] + "_"
        arcpy.AddMessage("Did not find the qualify_field_name() item in the Config files.")
        arcpy.AddMessage(in_table)
        exit(0)


def sanitize_fields(table):
    sanitize_list = []
    for fld in arcpy.ListFields(table):
        #arcpy.AddMessage(fld.type)
        if fld.type == "Guid":
            sanitize_list.append(fld.name)
    arcpy.AddMessage(sanitize_list)

def sanitize_recreate_fields(table, fieldlist):
    for fld in fieldlist:
        arcpy.AddField
            
    
def get_workspace():
    if os.path.basename(arcpy.env.scratchWorkspace).endswith("gdb", 3):
        return arcpy.env.scratchWorkspace
    else:
        return arcpy.env.scratchWorkspace + "\\scratch.gdb"


def build_overlays_iter(overlay_list, report_name, main_config, report_config, parent_path, environment):
    '''
        This is the main controlling function for the script.

        The helper functions called here are all built with the need to find previously overlayed results.
        Finding previous result is done through a counter variable/well known naming and shared workspace.
        
    '''
    counter = 0
    #counter variable is used for naming and finding overlay inputs for each run
    arcpy.AddMessage(" ")
    arcpy.AddMessage("#" + "*" * 45)
    arcpy.AddMessage("Number of Event Tables to Overlay: " + str(len(overlay_list)))
    arcpy.AddMessage("Starting..." + os.linesep)
    for ly in overlay_list:
        arcpy.AddMessage(str(counter + 1) + ". " + os.path.basename(ly).split(".")[-1][:-2])
        if counter == 0:
            if len(overlay_list) == 2:
                #This is when the overlay operation is the first and final
                final_overlay_name = finaloverlay(report_name, overlay_list, counter, main_config, report_config, parent_path, environment)
            else:
                #This is when the overlay operation is the first and NOT the final
                firstoverlay(overlay_list, report_name, counter, main_config)
        elif counter == 1:
            #Second layer gets overlayed in the firstoverlay() operation along with first layer so we pass here
            pass
        elif counter == len(overlay_list) - 1:
            #Last overlay needs to be detected before second overlay because second overlay may be last overlay
            #####################################
            ###
            ###Questions:   Can I push this overlay to the top to detect final overaly before first overlay
            ###             Final overlay/First overlay is different than Final overlay regular due to where the data is
            ###
            ###Answer:      Else condition for Final Overlay probably won't catch on Final overlay/First Overlay
            ###
            #####################################
            final_overlay_name = finaloverlay(report_name, ly, counter, main_config, report_config, parent_path, environment)
        elif counter == 2:
            #Second overlay of third layer which means we have to account for layer 1 & 2 done in firstoverlay()
            secondoverlay(report_name, ly, counter, main_config)
        else:
            #All the middle overlays!
            middleoverlay(report_name, ly, counter, main_config)
        counter += 1
    arcpy.AddMessage("#" + "*" * 45)
    arcpy.AddMessage(" ")
    return final_overlay_name


def firstoverlay(overlay_list, report_name, counter, main_config):
    global_wkspace = get_workspace()
    out_overlay_name = arcpy.CreateUniqueName(report_name + str(counter), global_wkspace)
    out_overlay_props = "RID" + str(counter) + " LINE From" + str(counter) +  " To" + str(counter)
    querytable0, props0 = prep_overlay(overlay_list[0], report_name, main_config)
    querytable1, props1 = prep_overlay(overlay_list[1], report_name, main_config)
    overlay(querytable0, props0, querytable1, props1, out_overlay_name, out_overlay_props, report_name, counter)


def secondoverlay(report_name, ly, counter, main_config):
    global_wkspace = get_workspace()
    common_props = "RID LINE BeginMeasure EndMeasure"
    querytable, props = prep_overlay(ly, report_name, main_config)
    out_overlay_name = arcpy.CreateUniqueName(report_name + str(counter), global_wkspace)
    out_overlay_props = "RID" + str(counter) + " LINE From" + str(counter) +  " To" + str(counter)
    in_overlay_name = global_wkspace + "\\" + report_name + str(counter - 2)
    in_overlay_props = "RID" + str(counter - 2) + " LINE From" + str(counter - 2) +  " To" + str(counter - 2)
    overlay(in_overlay_name, in_overlay_props, querytable, props, out_overlay_name, out_overlay_props, report_name, counter)


def middleoverlay(report_name, ly, counter, main_config):
    global_wkspace = get_workspace()
    out_overlay_name = arcpy.CreateUniqueName(report_name + str(counter), global_wkspace)
    out_overlay_props = "RID" + str(counter) + " LINE From" + str(counter) +  " To" + str(counter)
    in_overlay_name = global_wkspace + "\\" + report_name + str(counter - 1)
    in_overlay_props = "RID" + str(counter - 1) + " LINE From" + str(counter - 1) +  " To" + str(counter - 1)
    querytable, props = prep_overlay(ly, report_name, main_config)
    overlay(in_overlay_name, in_overlay_props, querytable, props, out_overlay_name, out_overlay_props, report_name, counter)


def finaloverlay(report_name, ly, counter, main_config, report_config, parent_path, environment):
    #This function was originally built with the fact that there would be a previous overlay result it
    #needed to find.  This is changing.
    global_wkspace = get_workspace()
    common_props = "RID LINE BeginMeasure EndMeasure"
    if len(ly) == 2:
        #ly is actually a list vs. a layer as is expected in my else statement
        in_overlay_name, in_overlay_props, querytable, props = finaloverlay_helper_case2(report_name, ly, counter, main_config, report_config, parent_path, environment)
    else:
        in_overlay_name, in_overlay_props, querytable, props = finaloverlay_helper_case1(report_name, ly, counter, main_config, report_config, parent_path, environment)
    
    final_overlay_name = assign_output(report_name, main_config, report_config, parent_path, environment)
    if arcpy.Exists(final_overlay_name):
        arcpy.Delete_management(final_overlay_name)
    overlay(in_overlay_name, in_overlay_props, querytable, props, final_overlay_name, common_props, report_name, counter)
    return final_overlay_name



def finaloverlay_helper_case2(report_name, overlay_list, counter, main_config, report_config, parent_path, environment):
    querytable0, props0 = prep_overlay(overlay_list[0], report_name, main_config)
    querytable1, props1 = prep_overlay(overlay_list[1], report_name, main_config)
    return querytable0, props0, querytable1, props1
    


def finaloverlay_helper_case1(report_name, ly, counter, main_config, report_config, parent_path, environment):
    global_wkspace = get_workspace()
    in_overlay_name = global_wkspace + "\\" + report_name + str(counter - 1)
    in_overlay_props = "RID" + str(counter - 1) + " LINE From" + str(counter - 1) +  " To" + str(counter - 1)
    querytable, props = prep_overlay(ly, report_name, main_config)
    if counter == 2:
        #Overwrite in_overlay_name and in_overlay_props to account for special situation of last overlay being the second overlay
        #which throws off how we find the previous overlayed data for the current overlay (previous result with next table)
        in_overlay_name = global_wkspace + "\\" + report_name + str(counter - 2)
        in_overlay_props = "RID" + str(counter - 2) + " LINE From" + str(counter - 2) +  " To" + str(counter - 2)
    return in_overlay_name, in_overlay_props, querytable, props


def prep_overlay(in_table, report_name, main_config):
    '''use report_name to differentiate MakeQueryTable in_memory names'''
    querytablename = report_name + "_" + os.path.basename(in_table).split(".")[-1] + "_VIEW"
    oid = os.path.basename(in_table) + "." + qualify_field_name(os.path.basename(in_table), main_config) + "ObjectID"
    if arcpy.Exists(querytablename):
        arcpy.Delete_management(querytablename)
    arcpy.MakeQueryTable_management(in_table, querytablename, "USE_KEY_FIELDS", oid, "", "")
    return querytablename, "RID LINE BeginMeasure EndMeasure"


def overlay(in1, inprops1, in2, inprops2, out1, outprops1, report_name, counter):
    global_wkspace = get_workspace()
    arcpy.OverlayRouteEvents_lr(in1, inprops1, in2, inprops2, "UNION", out1, outprops1, "NO_ZERO", "FIELDS", "INDEX")
    if arcpy.Exists(global_wkspace + "\\" + report_name + str(counter - 1)):
        arcpy.Delete_management(global_wkspace + "\\" + report_name + str(counter - 1))


def dynseg_start_flag(pid, report):
    output_db_conn = os.getcwd() + "\\GISCloudDEV_background_os.sde"
    flagtable = output_db_conn + "\\background.gisprocess.DYNSEG_FLAG"
    cursor = arcpy.da.InsertCursor(flagtable, ("PID" , "STARTTIME", "STATUS", "PROCESS_NAME"))
    cursor.insertRow(pid, datetime.datetime.now(), "RUNNING", report)



def getLogger(environment, config_dict):
    giscommon = config_dict["GISCOMMON"]
    logmodule = config_dict["LOGGINGMODULE"]
    logpath = config_dict["LOGGINGPATH"]
    full_logmod_path = os.path.join(giscommon, environment, logmodule)
    module_name = str(logmodule)[:-3]
    logger = imp.load_source(module_name, full_logmod_path)
    log = logger.LogIt(logpath)
    return log


def configbuilder(main_config_path, parent_path, environment):
    with open(main_config_path, "r") as file_reader:
        main_config = json.loads(file_reader.read())
    report_config = report_config_builder(main_config, parent_path, environment)
    return main_config, report_config


def report_config_builder(main_config, parent_path, environment):
    report_config = {}
    config_type_list = main_config["REPORTCONFIGS"]
    for i in config_type_list:
        report_config_path = os.path.join(parent_path + "\\" + environment + "\\" + main_config["WORKINGDIRECTORY"], i)
        with open(report_config_path, "r") as config_reader:
            config_item = json.loads(config_reader.read())
            report_config[config_item["REPORTNAME"]] = config_item
    return report_config


def test_permission():
    try:
        path = ""
        with arcpy.da.Editor(path) as editor:
            pass
    except:
        arcpy.AddMessage(" ")
        arcpy.AddMessage("WARNING!")
        arcpy.AddMessage("You do not have permission to run this Refresh Data tool.")
        arcpy.AddMessage(" ")
        exit(0)



if __name__ == "__main__":
    main()
