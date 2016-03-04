import arcpy
import toolbox_loader


for import_text in toolbox_loader.IMPORT_LIST:
    exec(import_text)


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "ageopyToolbox"
        self.alias = "ageopy"
        self.description = "ageopy Tools"
        self.tools = toolbox_loader.get_toolbox_classes()











