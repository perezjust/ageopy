import arcpy
import sys


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
        arcpy.AddMessage("here")
        arcpy.AddMessage(parameters[0].valueAsText)
        res = self.run_tool(parameters[0].valueAsText, parameters[1].valueAsText, parameters[2].valueAsText)
        '''
            It seems that the SetParameterAsText method generates a arcpy.Result object.
            I would like to instead return a json string...
        '''
        arcpy.SetParameterAsText(3, res)
        return


    def get_parameter(self, parameter, check_dataset, check_fc):
        parameter


    def run_tool(self, dbconn, check_dataset, check_fc):
        '''
            
        '''
        sys.stdout.write(check_dataset)
        arcpy.env.workspace = dbconn
        if check_dataset == True:
            dsVersioned, dsNotVersioned = self.is_dataset_versioned()
        else:
            dsVersioned = []
            dsNotVersioned = []
        if check_fc == True:
            itemVersioned, itemNotVersioned = self.is_items_versioned()
        else:
            itemVersioned = []
            itemNotVersioned = []
        return {"dsVersioned": dsVersioned, "dsNotVersioned": dsNotVersioned, "itemVersioned": itemVersioned, "itemNotVersioned": itemNotVersioned}


    def is_dataset_versioned(self):
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


    def is_items_versioned(self):
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






