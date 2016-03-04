

import arcpy
import datetime



def main():
    print datetime.datetime.now()
    iter_fcs()


def iter_fcs():
    conn = r"Database Connections\GISCloudQA_background_os.sde"
    arcpy.env.workspace = r"Database Connections\GISCloudQA_background_os.sde\background.GIS.Rextag"
    fcs = [fc.split(".")[-1] for fc in arcpy.ListFeatureClasses()]
    for fc in fcs:
        print str(fc) + "---" + str(sql_esri_createdate(conn, "GIS", fc))


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
    



if __name__ == "__main__":
    main()
