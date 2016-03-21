import arcpy
import sys
import os
import json
import webbrowser
import ast


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from esri import datastore
'''
    I think the architecture to clean this mess up
    is to create a bonafide package and have it installed
    which would update sys.path upon installation
'''


class VersioningHelperItemProperty(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Versioning Helper - Item Properties"
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
        displayName="Check Datasets",
        name="check_datasets",
        datatype="Boolean",
        parameterType="Optional",
        direction="Input")

        param2 = arcpy.Parameter(
        displayName="Check Feature Classes At Root",
        name="check_fc_at_root",
        datatype="Boolean",
        parameterType="Optional",
        direction="Input")

        param3 = arcpy.Parameter(
        displayName="Folder to Output JSON File",
        name="output_json_file",
        datatype="DEWorkspace",
        parameterType="Required",
        direction="Input")

        param4 = arcpy.Parameter(
        displayName="Output Features",
        name="out_features",
        datatype="String",
        parameterType="Derived",
        direction="Output")

        params = [param0, param1, param2, param3, param4]
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
        arcpy.AddMessage("here")
        arcpy.AddMessage(parameters[0].valueAsText)
        res = self.run_tool(parameters[0].valueAsText, parameters[1].value, parameters[2].value, parameters[3].valueAsText)
        '''
            It seems that the SetParameterAsText method generates a arcpy.Result object.
            I would like to instead return a json string...
        '''
        #arcpy.SetParameterAsText(4, res)
        return



    def run_tool(self, dbconn, check_tables_only, check_fcs_only, output_folder):
        check_list = []
        gdbbrowser = datastore.GDBBrowser(dbconn)
        if check_fcs_only == False and check_tables_only == True:
            check_list = gdbbrowser.tablelist
        if check_fcs_only == True and check_tables_only == False:
            check_list = gdbbrowser.fclist
        if check_fcs_only == True and check_tables_only == True:
            check_list = gdbbrowser.fclist + gdbbrowser.tablelist
        ###--Add a check and a message back to user if they choose False, False
        
        versioned_dict = self.is_item_versioned(check_list)
        #return versioned_list
        output_json_file = os.path.join(output_folder, "json.txt")
        if len(versioned_dict) > 0:
            json_data = json.dumps(versioned_dict)
            with open(output_json_file, 'w') as outfile:
                json.dump(json_data, outfile)
            webbrowser.open(output_json_file)
            return
        else:
            return []

        


    def is_item_versioned(self, check_list):
        ret_dict = {}
        versioned_list = []
        not_versioned_list = []
        for item in check_list:
            desc = arcpy.Describe(item)
            if desc.isVersioned == True:
                versioned_list.append(item)
            else:
                not_versioned_list.append(item)
        ret_dict["versioned"] = versioned_list
        return versioned_list







