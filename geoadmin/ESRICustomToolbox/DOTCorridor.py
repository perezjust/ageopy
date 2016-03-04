import os
import string
import sys
import traceback
import shutil
import logging
import os.path
import time
import arcpy
import arceditor


arcpy.env.overwriteOutput = True


def main():
    path = "O:\AppData\GIS\Cloud\Boardwalk\Workspace\GISScheduledTasks"
    mxd1 = path + "\\" + "GSP.mxd"
    mxd2 = path + "\\" + "TGT.mxd"
    mxd3 = path + "\\" + "GCP.mxd"
    mxdlist = [mxd1, mxd2]
    for mxd in mxdlist:
        refresh_target(mxd, path)
    



def refresh_target(mxd, path):
    try:
        item_dict = get_mxd_items(mxd)
        for item in item_dict:
            if item == "pods.GIS.StationSeries":
                infc = item_dict[item]
                operation(infc, mxd, path)
    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()


def operation(infc, mxd, path):
    arcpy.env.workspace = path
    company = os.path.basename(mxd).split(".")[0]
    print company
    generate_buffers(infc, path, company)


def generate_buffers(infc, path, company):
    output300 = path + "\\output\\" + company + "_300.shp"
    output660 = path + "\\output\\" + company + "_660.shp"
    arcpy.Buffer_analysis(infc, output300, "300 Feet", "FULL", "ROUND", "ALL", "pods.GIS.LineLoop.SystemCL")
    arcpy.Buffer_analysis(infc, output660, "660 Feet", "FULL", "ROUND", "ALL", "pods.GIS.LineLoop.SystemCL")
    update_final(output300, company, 300)
    update_final(output660, company, 660)


def update_final(infc, company, bufferDist):
    companyVal = '"' + company + '"'
    arcpy.AddField_management(infc, "BuffDist", "LONG", 5, "", "", "", "NULLABLE")
    arcpy.AddField_management(infc, "SystemCL", "TEXT", "", "", 10)
    arcpy.CalculateField_management(infc, "BuffDist", bufferDist, "PYTHON_9.3")
    arcpy.CalculateField_management(infc, "SystemCL", companyVal, "PYTHON_9.3")
    

def get_mxd_items(mxd):
    input_dict = {}
    get_layers(mxd, input_dict)
    get_tableviews(mxd, input_dict)
    return input_dict


def get_layers(mxd_path, input_dict):
    mxd = arcpy.mapping.MapDocument(mxd_path)
    df = arcpy.mapping.ListDataFrames(mxd, mxd.activeDataFrame.name)[0]
    for i in arcpy.mapping.ListLayers(mxd):
        input_dict[i.dataSource.split("\\")[-1]] = i
        #input_dict.append(i.dataSource.split("\\")[-1])
    return input_dict


def get_tableviews(mxd, input_dict):
    mxd = arcpy.mapping.MapDocument(mxd)
    df = arcpy.mapping.ListDataFrames(mxd, mxd.activeDataFrame.name)[0]
    for i in arcpy.mapping.ListTableViews(mxd):
        input_dict[i.dataSource.split("\\")[-1]] = i
        #input_list.append(i.dataSource.split("\\")[-1])
    return input_dict



if __name__ == "__main__":
    main()





