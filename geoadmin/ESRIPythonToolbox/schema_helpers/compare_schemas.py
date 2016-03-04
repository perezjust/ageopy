import arcpy




class ReportVersionsOffDefault1(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Report Child Versions Of Default1"
        self.description = ""
        self.canRunInBackground = False
        self.category = "PODS"
        
    def getParameterInfo(self):
        """Define parameter definitions"""


        DBConn = arcpy.Parameter(
            displayName = "Database Connection",
            name = "in_workspace",
            datatype = "Workspace",
            parameterType = "Required",
            direction = "Input")

        params = [DBConn]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
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
        val = 1
        return


##class SchemaHelperCompareSchemasTool(object):
##    def __init__(self):
##        """Define the tool (tool name is the name of the class)."""
##        self.label = "Refresh PODS Events To Maximo"
##        self.description = ""
##        self.canRunInBackground = False
##        self.category = "PODS"
##
##    def getParameterInfo(self):
##        """Define parameter definitions"""
##
##
##        DBConn = arcpy.Parameter(
##            displayName = "Database Connection",
##            name = "in_workspace",
##            datatype = "Workspace",
##            parameterType = "Required",
##            direction = "Input")
##
##        Route = arcpy.Parameter(
##            displayName = "Route",
##            name = "route",
##            datatype = "Feature Layer",
##            parameterType = "Required",
##            direction = "Input")
##
##        params = [DBConn, Route]
##        return params
##
##    def isLicensed(self):
##        """Set whether tool is licensed to execute."""
##        return True
##
##    def updateParameters(self, parameters):
##        """Modify the values and properties of parameters before internal
##        validation is performed.  This method is called whenever a parameter
##        has been changed."""
##        return
##
##    def updateMessages(self, parameters):
##        """Modify the messages created by internal validation for each tool
##        parameter.  This method is called after internal validation."""
##        return
##
##    def execute(self, parameters, messages):
##        """The source code of the tool."""
##        #import refresh_event_layers as reflayers
##        import testpackage.maximo_refresh_event_layers as reflayers
##        reflayers.pytmain(parameters)
##        return
##
##
