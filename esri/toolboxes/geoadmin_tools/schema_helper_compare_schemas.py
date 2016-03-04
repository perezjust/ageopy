import arcpy


class SchemaHelperCompareSchemas(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Schema Helper - Compare Schemas"
        self.description = ""
        self.category="GeoAdmin Tools"
        self.canRunInBackground = False


    def getParameterInfo(self):
    #Define parameter definitions

        # First parameter
        param0 = arcpy.Parameter(
        displayName="Input Features",
        name="in_features",
        datatype="Feature Layer",
        parameterType="Required",
        direction="Input")

        params = [param0]

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

        arcpy.AddMessage("Ha!")
        return











