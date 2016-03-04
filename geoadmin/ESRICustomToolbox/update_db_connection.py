import os
import string
import sys
import traceback
import shutil
import logging
import os.path
import time
import arcpy


def main():

    try:

        dbconn = arcpy.GetParameter(0)
        update_all_layers_switch = arcpy.GetParameter(1)
        update_layer_source(dbconn, update_all_layers_switch)


    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()


def update_layer_source(dbconn, update_all_layers_switch):
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd, mxd.activeDataFrame.name)[0]

    table_list = arcpy.mapping.ListTableViews(mxd, "", df)
    for ti in table_list:
            replace_datasource(ti, dbconn)
    
    if update_all_layers_switch == True:
        layer_list = arcpy.mapping.ListLayers(mxd, "", df)
    else:
        layer_list = arcpy.mapping.ListBrokenDataSources(mxd)
    for i in layer_list:
        replace_datasource(i, dbconn)
    mxd.save()
    arcpy.RefreshTOC()


def replace_datasource(lyr, dbconn):
    desc = arcpy.Describe(dbconn)
    dbtype = desc.workspaceFactoryProgID
    if dbtype == "esriDataSourcesGDB.SdeWorkspaceFactory.1":
        workspace_type = "SDE_WORKSPACE"
    elif dbtype == "esriDataSourcesGDB.FileGDBWorkspaceFactory.1":
        workspace_type = "FILEGDB_WORKSPACE"
    dbconn_path = desc.catalogPath
    try:

        lyr.replaceDataSource(dbconn_path, workspace_type)

    except:
        arcpy.AddMessage("Didn't Repair: " + str(lyr.name))
        arcpy.AddMessage(traceback.format_exc())



if __name__ == "__main__":
    main()





