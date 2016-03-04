import arcpy
import traceback
import os
import sys
import getpass

arcpy.env.overwriteOutput = True
arcpy.env.scratchWorkspace = os.getcwd()

def main():
    
    #Parameters
    datasource = arcpy.GetParameter(0)

    try:
        
        
        #datasource = r"C:\geoproc\GISCloudDev_pods_os.sde"
        events = str(datasource) + "\\" + "PODS_OMS.GIS.PipeSegment"
        route = str(datasource) + "\\" + r"PODS_OMS.GIS.Transmission\PODS_OMS.GIS.StationSeries"
        lineloop = str(datasource) + "\\" + "PODS_OMS.GIS.LineLoop"
        #output = refresh_linear_events(events, route, lineloop)
        #inspect_connection(datasource)
        arcpy.SetParameter(1, output)
        
               
    except:
        print traceback.format_exc()
        arcpy.AddMessage(traceback.format_exc())


def inspect_connection(datasource):
    for dirpath, dirnames, filenames in arcpy.da.Walk(datasource):
        arcpy.AddMessage("#" * 50)
        arcpy.AddMessage(filenames)



def refresh_linear_events(events, route, lineloop):
    rid = "rkey"
    props = "RouteEventID LINE BeginMeasure EndMeasure"
    lyr = "events"
    arcpy.MakeRouteEventLayer_lr(route, "EventID", events, props, lyr, "#", "#")
    for i in arcpy.Describe(lyr).fields:
        print i.name
##    arcpy.AddJoin_management(lyr, "RouteEventID" , route, "EventID")
##    print "++++++++++++++++++++++++++++++++++++++++++++++++++++"
##    for i in arcpy.Describe(lyr).fields:
##        print i.name
##    arcpy.AddJoin_management(lyr, "PODS.GIS.StationSeries.LineLoopEventID", lineloop, "EventID")
##    arcpy.CopyFeatures_management(lyr, "in_memory" + "\\refreshed")
##    return lyr


    





if __name__ == "__main__":
    main()
