
import os
import sys
import arcpy
import datetime


def main(*argv):
    """TODO: Add documentation about this function here"""
    try:
        
        iter_fcs()
        
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]




def iter_fcs():
    conn = r"Database Connections\GISCloudPROD_background_os.sde"
    arcpy.env.workspace = r"Database Connections\GISCloudPROD_background_os.sde\background.GIS.Rextag"
    fcs = [fc.split(".")[-1] for fc in arcpy.ListFeatureClasses()]
    for fc in fcs:
        print str(sql_esri_createdate(conn, "GIS", fc)) + "---" + str(fc) 


def sql_esri_createdate(connection, schema, table):
    sdeconn = arcpy.ArcSDESQLExecute(connection)

    storedproc = """DECLARE @DYNSEG_DATE DATETIME
    SET  @DYNSEG_DATE = (
    SELECT T.CREATE_DATE 

    FROM SYS.TABLES T 
    INNER JOIN SYS.SCHEMAS 
    S ON T.SCHEMA_ID=S.SCHEMA_ID 
    AND S.NAME = 'GIS' 
    AND T.NAME='""" + table + """' )

    SELECT @DYNSEG_DATE AS DYNSEG_DATE
    """

    return sdeconn.execute(storedproc)







if __name__ == '__main__':
    """
        # This test allows the script to be used from the operating
        # system command prompt (stand-alone), in a Python IDE, 
        # as a geoprocessing script tool, or as a module imported in
        # another script

        # Arguments are optional
    """
    argv = tuple(arcpy.GetParameterAsText(i)
        for i in range(arcpy.GetArgumentCount()))
    main(*argv)
