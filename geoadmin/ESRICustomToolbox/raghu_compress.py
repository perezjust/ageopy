import arcpy
import traceback
import os
import sys
import getpass
import shutil

arcpy.env.overwriteOutput = True


def main():


    try:
        
        route = arcpy.GetParameter(0)
        output_dir = arcpy.GetParameter(1)
        arcpy.env.scratchWorkspace = output_dir

        
        first_function()
        
               
    except:
        arcmessage(traceback.format_exc())




def first_funtion():
    print "Hi!"
    pass




##
##
##def manage_runtime_params(route, output_dir):
##    if get_arcpy_runtime() == "python":
##        output_dir1 = r""
##        route1 = r""
##    elif get_arcpy_runtime() == "arcmap":
##        output_dir1 = output_dir
##        route1 = route
##    return route1, output_dir1
##
##
##def refresh_events(route, output_dir):
##    '''
##        GOTCHA: This builds the tablelist from an mxd.  The event_dict doesn't necessarily reflect the mxd.
##    '''
##    if os.path.exists(str(output_dir) + "\\" + "scratch.gdb"):
##        shutil.rmtree(str(output_dir) + "\\" + "scratch.gdb")
##    tablelist = gettableviews()
##    for i in tablelist:
##        try:
##            #arcmessage("tableview: " + str(i))
##            refresh_linear_events(i, route, output_dir)
##        except:
##            arcmessage(traceback.format_exc())
##
##
##
##def build_source_destination_dict(route, output_dir):
##    routepath = arcpy.Describe(route).catalogPath
##    dbconnection = str(routepath).split(".sde")[0] + ".sde"
##    dbname = routepath.split("\\")[-1].split(".")[0]
##    podsnonedit = dbconnection + "\\" + dbname + ".MAXIMOPROCESS.PODSNonEdit" + "\\" + dbname + ".MaximoProcess.MX_"
##    podsroot = dbconnection + "\\" + dbname + ".MaximoProcess.MX_"
##    arcpy.env.workspace = str(output_dir) + "\\" + "scratch.gdb"
##    ret_dict = {}
##    for i in arcpy.ListFeatureClasses():
##        val = ""
##        if arcpy.Exists(podsnonedit + i) is True:
##            val = podsnonedit + i
##            #arcmessage(val)
##            #arcmessage(arcpy.Exists(val))
##        else:
##            val = podsroot + i
##            #arcmessage(val)
##            #arcmessage(arcpy.Exists(val))
##        ret_dict[i] = val
##    '''
##        ret_dict example
##        new: existing
##    '''
##    return ret_dict
##
##
##def refresh_linear_events(events, route, output_dir):
##    #arcmessage(arcpy.env.scratchWorkspace)
##    if is_linear(events) == "True":
##        props = "RouteEventID LINE BeginMeasure EndMeasure"
##    else:
##        props = "RouteEventID POINT Measure"
##    lyr = "events"
##    output_table = arcpy.Describe(events).name.split(".")[-1]
##    arcpy.MakeRouteEventLayer_lr(route, "EventID", events, props, output_table, "#", "#")
##    arcpy.CopyFeatures_management(output_table, "%scratchGDB%" + "\\" + output_table)
##
##
##def manage_persist_data(data_dict):
##    for i in data_dict:
##        persist_data(data_dict[i], i)
##
##
##def persist_data(existing, new):
##    arcmessage("existing: " + str(existing))
##    arcpy.DeleteFeatures_management(existing)
##    arcpy.Append_management(new, existing, "NO_TEST")
##
##
##def is_linear(event_table):
##        counter = 0
##        fieldnamelist = listfields(event_table)
##        if "BeginMeasure" in fieldnamelist:
##            counter += 1
##        if "EndMeasure" in fieldnamelist:
##            counter += 1
##        if counter == 2:
##            return "True"
##        else:
##            return "False"
##
##
##def arcmessage(message):
##    print message
##    arcpy.AddMessage(message)
##
##
##def gettableviews():
##    mxd = set_mxd()
##    df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
##    tablelist = arcpy.mapping.ListTableViews(mxd, "*", df)
##    return tablelist
##
##
##def listfields(event_table):
##        fldnamelist = []
##        for fi in arcpy.ListFields(event_table):
##            fldnamelist.append(fi.name)
##        return fldnamelist
##
##
##def get_arcpy_runtime():
##    if str(sys.executable).endswith("ArcMap.exe"):
##        executable = "arcmap"
##    elif str(sys.executable).endswith("pythonw.exe"):
##        executable = "python"
##    return executable
##
##
##def set_mxd():
##    if get_arcpy_runtime() == "python":
##        mxdpath = r"PODS_EventTables_For_Maximo.mxd"
##        mxd = arcpy.mapping.MapDocument(mxdpath)
##    elif get_arcpy_runtime() == "arcmap":
##        mxd = arcpy.mapping.MapDocument("CURRENT")
##    return mxd
##
##
##    





if __name__ == "__main__":
    main()
