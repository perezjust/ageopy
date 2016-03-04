# -*- coding: ascii -*-
"""
Python Toolbox
"""


__author__ = 'Integrated Informatics Inc.'


import sys
from os.path import dirname
try:
    file_name = __file__
except NameError:
    file_name = sys.argv[0]
sys.path.insert(0, dirname(dirname(file_name)))
# NOTE import everything, explicitly set __all__ set to avoid collisions
from schema_helpers.compare_schemas import *


__all__ = ['Toolbox']


TOOLS = [t for t in globals().values() if hasattr(t, 'getParameterInfo')]


class Toolbox(object):
    """
    Toolbox, toolbox name is the name of the script.
    """
    def __init__(self):
        """
        Initialize the Toolbox
        """
        self.alias = u'alias'
        self.label = u'Toolbox Label'
        self.tools = TOOLS
    # End init built-in
# End Toolbox class


if __name__ == '__main__':
    Toolbox()
