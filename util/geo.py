import os
import string
import sys
import shutil
import logging
import datetime
import traceback
from collections import defaultdict

import json
from pprint import pprint




def main():
    v = "Is this by convention?"


def EsriJsonToLeafletJson(src, shapetype, attributes=None):
    with open(src) as data_file:
        geodata = json.load(data_file)

    leafjson = {}
    leafjson["type"] = "FeatureCollection"
    
    features = []
    counter = 1
    
    for i in geodata["features"]:
        if counter <> 0:
            esri_json_geom = i["geometry"]
            
            new_prop = ESRIJsonAttributeHelper(attributes, i["attributes"])

            new_geom = ESRIJsonGeomHelper(shapetype, esri_json_geom)

            if len(new_geom) > 0:
                new_feat = {}
                new_feat["geometry"] = new_geom
                new_feat["type"] = "Feature"
                new_feat["properties"] = new_prop
                new_feat["id"] = counter
                features.append(new_feat)
            counter += 1
        
    leafjson["features"] = features
    return json.dumps(leafjson)



def ESRIJsonAttributeHelper(attribute_order, esri_json_attributes):
    attrs = []
    for i in attribute_order:
        if esri_json_attributes[i] is not None:
            attrs.append(esri_json_attributes[i])
    return " - ".join(attrs)
       


def ESRIJsonGeomHelper(shapetype, esri_json_geom):
    if shapetype == "Point":
        new_geom = {}
        new_geom["type"] = "Point"
        new_geom["coordinates"] = [esri_json_geom["x"], esri_json_geom["y"]]
        if esri_json_geom["x"] == "NaN" or esri_json_geom["y"] == "NaN":
            new_geom = {}
        return new_geom
    elif shapetype == "Polyline":
        new_geom = {}
        new_geom["type"] = "LineString"
        coordslist = []
        for coords in esri_json_geom["paths"][0]:
            coordslist.append(coords)
        new_geom["coordinates"] = coordslist
        return new_geom
            
        



if __name__ == "__main__":
    main()
