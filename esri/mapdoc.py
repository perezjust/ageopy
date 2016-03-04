'''Create code re-use library for ArcGIS stuff

    regular class methods take self as the first argument

    class variables shares the data across all instances

    class method (@classmethod above the def statement)can be used to construct python classes in differing ways.  A @classmethod def
    for each constuctor need should use the return cls(parameter) statement to allow the construction of the subclass

    if my class functions don't use self in the logic, it is quite probable that it should be a @staticmethod that needs to
    know nothing about a instance of a class but putting it in the class definition can help users find the method if that's appropriate

    class local method is the dunder method

    @property

    flyweight design pattern supresses the instance dictionary by using __slots__ which don't inherit dict


    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    1. Handler to easily switch from file gdb to shapefile to sde feature class name - handle db schema naming
    2. 

    
'''

import arcpy
import os
import string
import sys
import traceback
from os.path import join
import arceditor





class MapDoc(object):
    '''
    Create a map document object from any geo lib

    TODO:   Implement this to detect the potential map package then inherit from proper class...if that
            is even the appropriate workflow

    '''

    version = '0.1'
    


    def __init__(self, path, dataframe=None):
        '''Instance variables that would be unique to an instance of mapdoc'''
        self.mappath = path
        self.mapobject = self.set_mapobject()
        self.mappackage = ""



    def printtest(self):
        print self.mappath
        arcpy.AddMessage(self.mappath)



    def set_mapobject(self, mappath=None):
        mapobject = arcpy.mapping.MapDocument(self.mappath)
        return mapobject

        

    def set_default_dataframe(self, dataframe=None):
        pass
        


    def get_layers(self, dataframe=None):
        mxd = self.mapobject
        df = arcpy.mapping.ListDataFrames(mxd, mxd.activeDataFrame.name)[0]
        if dataframe != None:
            df = arcpy.mapping.ListDataFrames(mxd, dataframe)[0]
        layer_list = arcpy.mapping.ListLayers(mxd, "", df)
        return layer_list


    def set_layer_sql(self, layer, value, field, operator):
        if layer.supports("definitionQuery"):
            flddel = arcpy.AddFieldDelimiters(layer.dataSource, field)
            sql = flddel + """ """ + operator + """ """ + """'{}'""".format(value)
            currentDefQuery = layer.definitionQuery
            if currentDefQuery != "":
                layer.definitionQuery = currentDefQuery + " AND " + sql
            else:
                layer.definitionQuery = sql
            arcpy.AddMessage(str(layer.name) + " == " + str(layer.definitionQuery))
            

    def save(self, new_mxd=None):
        self.mapobject.save()
    
        









