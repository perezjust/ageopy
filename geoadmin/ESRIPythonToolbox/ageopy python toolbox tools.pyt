import arcpy
import imp
import os

import sys
from os.path import dirname
try:
    file_name = __file__
except NameError:
    file_name = sys.argv[0]
sys.path.insert(0, dirname(dirname(file_name)))
# NOTE import everything, explicitly set __all__ set to avoid collisions

sys.path.insert(0, os.path.join(dirname(file_name), "schema_helpers"))


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "ageopy ESRI Tools"
        self.alias = "This is awesome"

        # List of tool classes associated with this toolbox
        from schema_helpers.compare_schemas import ReportVersionsOffDefault1
        self.tools = [ReportVersionsOffDefault1]








if __name__ == '__main__':
    Toolbox()











