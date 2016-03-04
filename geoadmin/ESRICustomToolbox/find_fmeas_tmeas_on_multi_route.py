import arcpy
import os
import string
import sys
import traceback
from os.path import join


import expFuncs as expF
from expFuncs import *
import gpFuncs as gpF
from gpFuncs import *

exp = meiSetUp("multi_route_measure")





def main():
    arcpy.env.workspace = "in_memory"
    path = arcpy.GetParameter(0)
    route = arcpy.GetParameter(1)
    rid_field = arcpy.GetParameter(2)
    func1(path, route, rid_field)


def func1(path, route, rid_field):
    with arcpy.da.UpdateCursor(path,("FMEAS", "TMEAS", "SHAPE@")) as rows:
        for i,row in enumerate(rows):
            print row[2]
            if row[2].partCount == 1:          
                for part in row[2]:
                    #part.count is the number of vertices
                    pntCount = part.count
                    count = 0
                    for pnt in part:
                        count += 1
                        if count == 1:
                            fmeas = create_point(pnt.Y, pnt.X, path, route, rid_field)
                            row[0] = fmeas
                        elif count == pntCount:
                            tmeas = create_point(pnt.Y, pnt.X, path, route, rid_field)
                            row[1] = tmeas
                    if (tmeas - fmeas) < 0:
                        arcpy.AddMessage("The From station is greater than the To station.")
                    #row[4] = tmeas - fmeas
                    del fmeas, tmeas
            else:
                arcpy.AddMessage("This tool is not built to handle multipart features.")
            rows.updateRow(row)


def get_measure_from_route(feature_layer, route, rid_field):
    table = arcpy.CreateUniqueName("table", "in_memory")
    props = "RID POINT MEAS"
    arcpy.LocateFeaturesAlongRoutes_lr(feature_layer, route, rid_field, "5 FEET", table, props)
    measure = read_table(table)
    return measure

def create_point(lat, lon, fc, route, rid_field):
    arcpy.env.workspace = "in_memory"
    point = arcpy.Point()
    point.X = lon
    point.Y = lat
    pnt_geom_list = []
    pnt_geometry = arcpy.PointGeometry(point)
    pnt_geom_list.append(pnt_geometry)
    print pnt_geom_list
    fl = arcpy.CreateUniqueName("point")
    arcpy.CopyFeatures_management(pnt_geom_list, fl)
    point_lyr = arcpy.CreateUniqueName(os.path.basename(fl)+ "xo")
    arcpy.MakeFeatureLayer_management(fl, point_lyr)
    measure = get_measure_from_route(point_lyr, route, rid_field)
    return measure

def read_table(table):
    for i in arcpy.SearchCursor(table):
        measure = i.getValue("MEAS")
        series = i.getValue("RID")
    return measure
    

          


if __name__ == "__main__":
    main()



