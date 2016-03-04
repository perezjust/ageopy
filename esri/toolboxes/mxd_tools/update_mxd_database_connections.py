import arcpy


class UpdateMXDDatabaseConnections(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Update MXD Database Connections"
        self.description = ""
        self.category="MXD Tools"
        self.canRunInBackground = False

    

    def isLicensed(self):
        return True


    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        if parameters[3].value:
            parameters[5].enabled = 0
            parameters[5].filter.list = [" "]
            parameters[5].value = " "
            parameters[6].enabled = 0
            parameters[6].filter.list = [" "]
            parameters[6].value = " "
        else:
            if parameters[4].value:
                number_fields_list = ['Short', 'Long', 'Float', 'Single', 'Double']
                valid_field_names = []
                pipe_table_fields_list = arcpy.ListFields(parameters[4].valueAsText)
                for field in pipe_table_fields_list:
                    if field.type in number_fields_list:
                        valid_field_names.append(field.name)
                parameters[5].filter.list = valid_field_names
                parameters[6].filter.list = valid_field_names
                parameters[5].enabled = 1
                parameters[6].enabled = 1


        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""


        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        arcpy.AddMessage("Ha!")
        return

 













