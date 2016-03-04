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




def main(report_name, main_config_path, parent_path, environment, execute_sp_flag):
    try:
        ##log = logger.LogIt("\\\\aws0fspv1.boardwalk.corp\\Shared$\\AppData\\GIS\\Cloud\\Software\\Boardwalk\\AppLogs\\agsreportdatarefresh-dev")
        ##THIS IS A MIGRATION TEST LINE EDIT##
        main_config, report_config = configbuilder(main_config_path, parent_path, environment)

        logpypath = main_config["LOGGINGMODULE"] + "\\" + environment + "\\" + "bwp_logging.py"
        logger = imp.load_source("bwp_logging", logpypath)
        
        report_item_list = report_config[report_name]["REPORTLIST"]
        report_list_full_path = []
        for report_item in report_item_list:
            report_list_full_path.append(os.path.join(parent_path + "\\" + environment + "\\" + main_config["DATABASECONNECTIONFOLDER"], environment + "_" + main_config["BACKGROUNDSDE"], main_config[report_item][0]))
        if execute_sp_flag == True:
            arcpy.AddMessage(execute_sp_flag)
        build_overlays(report_list_full_path, report_name, main_config, report_config, parent_path, environment, execute_sp_flag)
    except:
        print traceback.format_exc()
        arcpy.AddMessage(traceback.format_exc())
        #log.logMessage(traceback.format_exc())




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


def build_overlays(in_table_list, report_name, main_config, report_config, parent_path, environment, execute_sp_flag):
    #test_permission()
    overlay_table = build_overlays_iter(in_table_list, report_name, main_config, report_config, parent_path, environment)
    addmilepostfields(overlay_table)
    if execute_sp_flag == True:
        execute_storedproc(report_name, main_config, report_config, parent_path, environment)


def addmilepostfields(final_table):
    arcpy.AddField_management(final_table, "BeginMilePost", "LONG", "", "", "", "")
    arcpy.AddField_management(final_table, "BeginPlusFootage", "LONG", "", "", "", "")
    arcpy.AddField_management(final_table, "EndMilePost", "LONG", "", "", "", "")
    arcpy.AddField_management(final_table, "EndPlusFootage", "LONG", "", "", "", "")


def execute_storedproc(report_name, main_config, report_config, parent_path, environment):
    path = parent_path + "\\" + environment + "\\" + main_config["DATABASECONNECTIONFOLDER"]
    outputdb = os.path.join(path, environment + "_" + main_config["DYNSEGSDE"])
    sdeconn = arcpy.ArcSDESQLExecute(outputdb)
    storedproc = "execute dynseg.usp_ODM_REFRESH " + report_config[report_name]["STOREDPROC"]
    try:
        ret = sdeconn.execute(storedproc)
    except AttributeError:
        arcpy.AddMessage("")
        arcpy.AddMessage("!!!")
        arcpy.AddMessage("Please try again momentarily.  Another User is running the " + report_name + " Refresh Data Report.")
        arcpy.AddMessage("!!!")
        arcpy.AddMessage("")
        exit(0)
    

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


def get_workspace():
    #arcpy.AddMessage(os.path.basename(arcpy.env.scratchWorkspace))
    if os.path.basename(arcpy.env.scratchWorkspace).endswith("gdb", 3):
        return arcpy.env.scratchWorkspace
    else:
        return arcpy.env.scratchWorkspace + "\\scratch.gdb"


def build_overlays_iter(overlay_list, report_name, main_config, report_config, parent_path, environment):
    '''
        This is the main controlling function for the script.

        *- USAGE -*
        This function will break if the first overlay is the last overlay (ie two inputs only)
        *- USAGE -*
        
        There is a workspace rule that the middle_overlay and final_overlay have hardcoded in each.
        It basically switches where the output will write to.
        
    '''
    counter = 0
    arcpy.AddMessage(" ")
    arcpy.AddMessage("#" + "*" * 45)
    arcpy.AddMessage("Number of Event Tables to Overlay: " + str(len(overlay_list)))
    arcpy.AddMessage("Starting..." + os.linesep)
    for ly in overlay_list:
        arcpy.AddMessage(str(counter + 1) + ". " + os.path.basename(ly).split(".")[-1][:-2])
        #arcpy.AddMessage(counter)
        if counter == 0:
            #overlay numero uno (number one)
            firstoverlay(overlay_list, report_name, counter, main_config)
        elif counter == 1:
            #Second layer gets overlayed in the firstoverlay() operation along with first layer so we pass here
            pass
        elif counter == len(overlay_list) - 1:
            #Last overlay.  If also the third iteration, counter=2, then a bit of extra code needed in finaloverlay
            arcpy.AddMessage("#" + "*" * 45)
            arcpy.AddMessage(" ")
            final_overlay_name = finaloverlay(report_name, ly, counter, main_config, report_config, parent_path, environment)
        elif counter == 2:
            #Second overlay of third layer which means we have to account for layer 1 & 2 done in firstoverlay()
            secondoverlay(report_name, ly, counter, main_config)#, overlay_list)
        else:
            #All the middle overlays!
            middleoverlay(report_name, ly, counter, main_config)
        counter += 1
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
    global_wkspace = get_workspace()
    common_props = "RID LINE BeginMeasure EndMeasure"
    in_overlay_name = global_wkspace + "\\" + report_name + str(counter - 1)
    in_overlay_props = "RID" + str(counter - 1) + " LINE From" + str(counter - 1) +  " To" + str(counter - 1)
    querytable, props = prep_overlay(ly, report_name, main_config)
    if counter == 2:
        in_overlay_name = global_wkspace + "\\" + report_name + str(counter - 2)
        in_overlay_props = "RID" + str(counter - 2) + " LINE From" + str(counter - 2) +  " To" + str(counter - 2)
    final_overlay_name = assign_output(report_name, main_config, report_config, parent_path, environment)
    if arcpy.Exists(final_overlay_name):
        arcpy.Delete_management(final_overlay_name)
    overlay(in_overlay_name, in_overlay_props, querytable, props, final_overlay_name, common_props, report_name, counter)
    return final_overlay_name


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




if __name__ == "__main__":
    main()
