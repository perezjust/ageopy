import os
import sys
from collections import defaultdict
import json
import ast

#local libs
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ageopy.util import filesys


class GPErrorDict(object):
    
    def __init__(self):
        '''
            group errors so they can be reported in organized way
            useful when try/excepting through a geoprocessing operation
            against items
        '''
        self.errordict = defaultdict(list)
        

    def add(self, messagelist):
        error = messagelist[0]
        item = messagelist[1]
        self.errordict[error].append(item)


    def write_to_disk(self, outputfolder):
        errorfile = os.path.join(outputfolder, "error_" + filesys.get_nice_date("Alt") + ".txt")
        with open(errorfile, 'w') as outfile:
            for dictitem in self.errordict:
                outfile.write(str(dictitem) + '\n')
                for listitem in self.errordict[dictitem]:
                    outfile.write(str(listitem) + '\n')
                outfile.write('\n')
                outfile.write("+" * 100)
                outfile.write('\n')
        return errorfile


def ESRIJsonToShapefile(source_files):
    for fi in source_files:
        with open(fi) as data_file:
            geodata = ast.literal_eval(data_file.read())


def EsriJsonToLeafletJson(source_files, shapetype, attributes=None):
    '''
        Sample call:

            sys.path.append(r"\\boardwalk.corp\global\AppData\GIS\Cloud\Users\PerezJ\gh")
            import ageopy.esri.helpers as esri_helper
            import ageopy.util.filesys as filesys
            file_list = []
            bikeattrs = ["Legend", "FULL_NAME"]
            file_list = filesys.build_walk_list(r"C:\bikehou", "txt")
            res = esri_helper.EsriJsonToLeafletJson(file_list, "Polyline", bikeattrs)

            with open(r"c:\houbike.txt", 'w') as f:
                f.write("var houbike = ")
                f.write(res)
                f.write(";")
                
    '''
    leafjson = {}
    leafjson["type"] = "FeatureCollection"
    features = []
    
    for fi in source_files:
        with open(fi) as data_file:
            geodata = ast.literal_eval(data_file.read())
        
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
                    if new_prop["Legend"] == "Shared-Use Paths":
                        features.append(new_feat)
                counter += 1
            
    leafjson["features"] = features
    return json.dumps(leafjson)



def ESRIJsonAttributeHelper(attribute_order, esri_json_attributes):
    attrs = {}
    for i in attribute_order:
        attrs[i] = esri_json_attributes[i]
    return attrs



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



def gulp_to_disk(dictio):
    '''
        Duplicate functionality as EsriJsonToLeafletJson()
    '''
    features = dictio["features"]
    geomtype = dictio["geometryType"]
    if geomtype == "esriGeometryPolygon":
        print geomtype
        for f in features:
            attributes = f["attributes"]
            geo = f["geometry"]["rings"]


    with open(r"C:\bikehou\0.txt") as f:
        dictio = ast.literal_eval(f.read())
        gulp_to_disk(dictio)

        
