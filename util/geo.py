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

data = r"\\boardwalk.corp\global\AppData\GIS\Cloud\Users\PerezJ\gh\data\tx_boat_ramps.json.txt"


def main():
    pprint(EsriJsonToLeafletJson(data))


def EsriJsonToLeafletJson(src):
    with open(data) as data_file:
        geodata = json.load(data_file)

    leafjson = {}
    leafjson["type"] = "FeatureCollection"
    
    features = []
    counter = 1
    for i in geodata["features"]:
        src_geom = i["geometry"]
        name = i["attributes"]["LocName"]
        desc = i["attributes"]["GPS_PntTyp"]
        if desc is None:
            desc = "No Description"
        if name is None:
            name = "No Name"
        '''
            Build attributes
        '''
        new_prop = {}
        new_prop["popupContent"] = str(name) + " - " + str(desc)
        new_coords = []
        new_geom = {}
        new_geom["type"] = "Point"
        #new_geom1["coordinates"] = [src_geom["x"], src_geom["y"]]
        new_geom["coordinates"] = ["-95.92280555555556", "29.939716666666666"]
        '''
            Insert feature
        '''
        new_feat = {}
        new_feat["geometry"] = new_geom
        new_feat["type"] = "Feature"
        new_feat["properties"] = new_prop
        new_feat["id"] = counter
        features.append(new_feat)
        counter += 1

    leafjson["features"] = features
    
    return json.dumps(leafjson)




if __name__ == "__main__":
    main()
