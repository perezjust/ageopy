import arcpy
import sys
import os
import traceback

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from esri import datastore
'''
    I think the architecture to clean this mess up
    is to create a bonafide package and have it installed
    which would update sys.path upon installation
'''



class VersioningHelperUnregisterItems(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Versioning Helper - Unregister Items"
        self.description = ""
        self.category="GeoAdmin Tools"
        self.canRunInBackground = False
        self.alias = "ageopy"


    def getParameterInfo(self):
        param0 = arcpy.Parameter(
        displayName="Enterprise Database Connection",
        name="in_sde",
        datatype="DEWorkspace",
        parameterType="Required",
        direction="Input")

        param1 = arcpy.Parameter(
        displayName="Unregister Tables Only",
        name="unregister_tables",
        datatype="Boolean",
        parameterType="Optional",
        direction="Input")

        param2 = arcpy.Parameter(
        displayName="Unregister Feature Classes Only",
        name="unregister_fcs",
        datatype="Boolean",
        parameterType="Optional",
        direction="Input")

        param3 = arcpy.Parameter(
        displayName="Output Features",
        name="out_features",
        datatype="String",
        parameterType="Derived",
        direction="Output")

        params = [param0, param1, param2, param3]
        return params


    

    def isLicensed(self):
        return True
        

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        return


    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        return


    def execute(self, parameters, messages):
        """The source code of the tool."""
        
        res = self.run_tool(parameters[0].valueAsText, parameters[1].value, parameters[2].value)
        '''
            It seems that the SetParameterAsText method generates a arcpy.Result object.
            I would like to instead return a json string...
        '''
        arcpy.SetParameterAsText(3, res)
        return


    def get_parameter(self, parameter, check_dataset, check_fc):
        '''
            not implemented
        '''
        parameter


    def run_tool(self, dbconn, unreg_tables_only, unreg_fcs_only):
        '''
            Keeps execute method clean
        '''
        arcpy.env.workspace = dbconn
        total_list = []
        gdbbrowser = datastore.GDBBrowser(dbconn)
        if unreg_fcs_only == False and unreg_tables_only == True:
            total_list = gdbbrowser.tablelist
        if unreg_fcs_only == True and unreg_tables_only == False:
            total_list = gdbbrowser.fclist
        if unreg_fcs_only == True and unreg_tables_only == True:
            total_list = gdbbrowser.fclist + gdbbrowser.tablelist
        return total_list


    def get_full_tablelist(self):
        is_versioned = []
        is_not_versioned = []
        for i in arcpy.ListDatasets():
            try:
                datasetVersioned = arcpy.Describe(i).isVersioned
                if datasetVersioned == False:
                    is_not_versioned.append(i)
                else:
                    is_versioned.append(i)

            except:
                arcpy.AddMessage(traceback.format_exc())
                print traceback.format_exc()
        return is_versioned, is_not_versioned


    def get_full_fclist(self):
        is_versioned = []
        is_not_versioned = []
        for j in arcpy.ListTables():
            try:
                
                tableVersioned = arcpy.Describe(j).isVersioned
                if tableVersioned == False:
                    is_not_versioned.append(j)
                else:
                    is_versioned.append(j)

            except:
                arcpy.AddMessage(traceback.format_exc())
                print traceback.format_exc()
                
        for y in arcpy.ListFeatureClasses():
            try:
                
                tableVersioned = arcpy.Describe(y).isVersioned
                if tableVersioned == False:
                    is_not_versioned.append(y)
                else:
                    is_versioned.append(y)

            except:
                arcpy.AddMessage(traceback.format_exc())
                print traceback.format_exc()
        
        return is_versioned, is_not_versioned






