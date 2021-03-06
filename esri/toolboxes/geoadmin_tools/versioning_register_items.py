import arcpy
import sys
import os
import traceback
import json
import ast
import webbrowser

#local libs
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from esri import datastore
from esri import helpers
from util import filesys
'''
    I think the architecture to clean this mess up
    is to create a bonafide package and have it installed
    which would update sys.path upon installation
'''



class VersioningRegisterItems(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Versioning - Register Items"
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
        displayName="Folder to Output Error File",
        name="error_file_folder",
        datatype="DEWorkspace",
        parameterType="Required",
        direction="Input")

        param2 = arcpy.Parameter(
        displayName="Register Tables",
        name="register_tables",
        datatype="Boolean",
        parameterType="Optional",
        direction="Input")

        param3 = arcpy.Parameter(
        displayName="Register Feature Classes",
        name="register_fcs",
        datatype="Boolean",
        parameterType="Optional",
        direction="Input")

        param4 = arcpy.Parameter(
        displayName="JSON List To Register As Versioned",
        name="json_versioned_items",
        datatype="DETextfile",
        parameterType="Optional",
        direction="Input")

        param5 = arcpy.Parameter(
        displayName="No Output",
        name="output_list",
        datatype="String",
        parameterType="Derived",
        direction="Output")

        param2.value = True
        param3.value = True

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
        
        res = self.run_tool(parameters[0].valueAsText, parameters[1].valueAsText, parameters[2].value, parameters[3].value, parameters[4].valueAsText)
        '''
            It seems that the SetParameterAsText method generates a arcpy.Result object.
            I would like to instead return a json string...
        '''
        #arcpy.SetParameterAsText(4, res)
        return



    def run_tool(self, dbconn, errors_folder, reg_tables_only, reg_fcs_only, json_versioned_items):
        '''
            Keeps execute method clean.

            
        '''
        if json_versioned_items is not None:
            with open(json_versioned_items) as readme:
                d = json.loads(readme.read())
            raw_list = ast.literal_eval(d)
        else:
            raw_list = self.control_flow(dbconn, reg_tables_only, reg_fcs_only)
        register_list = self.organize_register_plan(dbconn, raw_list)
        gp_error_dict = self.register_items(register_list)
        self.handle_gp_errors(gp_error_dict, errors_folder)
        return


    def handle_gp_errors(self, gp_error_dict, error_folder):
        error_file = gp_error_dict.write_to_disk(error_folder)
        webbrowser.open(error_file)


    def register_items(self, register_list):
        gp_error_dict = helpers.GPErrorDict()
        for i in register_list:
            try:
                #Very important here to pass third parameter as "" empty
                arcpy.RegisterAsVersioned_management(i, "NO_EDITS_TO_BASE")
                arcpy.AddMessage("Registered -- " + str(i))
            except:
                gp_error_dict.add([traceback.format_exc(), i])
        return gp_error_dict

        


    def organize_register_plan(self, dbconn, versioned_list):
        '''
            Account for the fact that ArcSDE Versioned items are organized at the
            ArcSDE Feature Dataset level.  Unregister a Feature Dataset or a table/featureclass
            that lives at the Root of ArcSDE.
        '''
        register_list = []
        for item in versioned_list:

            #If dirname_of_item == dbconn then the item is at root of SDE
            #This will probably break if the sde file is not located in a two level folder structure
            dirname_of_item = os.path.dirname(item)
            if dirname_of_item == str(dbconn):
                if item not in register_list:
                    register_list.append(item)
            else:
                if os.path.dirname(item) not in register_list:
                    register_list.append(os.path.dirname(item))

        return register_list
            


    def control_flow(self, dbconn, reg_tables_only, reg_fcs_only):
        arcpy.env.workspace = dbconn
        total_list = []
        gdbbrowser = datastore.GDBBrowser(dbconn)
        if reg_fcs_only == False and reg_tables_only == True:
            total_list = gdbbrowser.tablelist
        if reg_fcs_only == True and reg_tables_only == False:
            total_list = gdbbrowser.fclist
        if reg_fcs_only == True and reg_tables_only == True:
            total_list = gdbbrowser.fclist + gdbbrowser.tablelist
        return total_list









