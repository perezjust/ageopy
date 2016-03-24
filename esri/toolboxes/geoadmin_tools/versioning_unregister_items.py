import arcpy
import sys
import os
import traceback
import json
import ast

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from esri import datastore
'''
    I think the architecture to clean this mess up
    is to create a bonafide package and have it installed
    which would update sys.path upon installation
'''



class VersioningUnregisterItems(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Versioning - Unregister Items"
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
        displayName="Unregister Tables",
        name="unregister_tables",
        datatype="Boolean",
        parameterType="Optional",
        direction="Input")

        param2 = arcpy.Parameter(
        displayName="Unregister Feature Classes",
        name="unregister_fcs",
        datatype="Boolean",
        parameterType="Optional",
        direction="Input")

        param3 = arcpy.Parameter(
        displayName="JSON List To Unregister As Versioned",
        name="json_versioned_items",
        datatype="DETextfile",
        parameterType="Optional",
        direction="Input")

        param4 = arcpy.Parameter(
        displayName="No Output",
        name="output_list",
        datatype="String",
        parameterType="Derived",
        direction="Output")

        param1.value = True
        param2.value = True

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
        
        res = self.run_tool(parameters[0].valueAsText, parameters[1].value, parameters[2].value, parameters[3].valueAsText)
        '''
            It seems that the SetParameterAsText method generates a arcpy.Result object.
            I would like to instead return a json string...
        '''
        #arcpy.SetParameterAsText(4, res)
        return



    def run_tool(self, dbconn, unreg_tables_only, unreg_fcs_only, json_versioned_items):
        '''
            Keeps execute method clean
        '''
        if json_versioned_items == "":
            with open(json_versioned_items) as readme:
                d = json.loads(readme.read())
            raw_list = ast.literal_eval(d)
        else:
            raw_list = self.control_flow(dbconn, unreg_tables_only, unreg_fcs_only)
        unregister_list = self.organize_unregister_plan(dbconn, raw_list)
        self.unregister_items(unregister_list)
        return


    def unregister_items(self, unregister_list):
        for i in unregister_list:
            try:
                #Very important here to pass third parameter as "" empty
                arcpy.UnregisterAsVersioned_management(i, "KEEP_EDIT", "")
                arcpy.AddMessage("Unregistered -- " + str(i))
            except:
                arcpy.AddMessage(i)
                arcpy.AddMessage("--")
                arcpy.AddMessage(traceback.format_exc())

        


    def organize_unregister_plan(self, dbconn, versioned_list):
        '''
            Account for the fact that ArcSDE Versioned items are organized at the
            ArcSDE Feature Dataset level.  Unregister a Feature Dataset or a table/featureclass
            that lives at the Root of ArcSDE.
        '''
        unregister_list = []
        for item in versioned_list:

            #If dirname_of_item == dbconn then the item is at root of SDE
            #This will probably break if the sde file is not located in a two level folder structure
            dirname_of_item = os.path.dirname(item)
            if dirname_of_item == str(dbconn):
                if item not in unregister_list:
                    unregister_list.append(item)
            else:
                if os.path.dirname(item) not in unregister_list:
                    unregister_list.append(os.path.dirname(item))

        return unregister_list
            


    def control_flow(self, dbconn, unreg_tables_only, unreg_fcs_only):
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






