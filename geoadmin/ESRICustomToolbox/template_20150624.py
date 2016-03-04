
import os
import sys
import arcpy


def main(*argv):
    """TODO: Add documentation about this function here"""
    try:
        
        do_analysis()
        
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]




def do_analysis():
    pass




if __name__ == '__main__':
    """
        # This test allows the script to be used from the operating
        # system command prompt (stand-alone), in a Python IDE, 
        # as a geoprocessing script tool, or as a module imported in
        # another script

        # Arguments are optional
    """
    argv = tuple(arcpy.GetParameterAsText(i)
        for i in range(arcpy.GetArgumentCount()))
    main(*argv)
