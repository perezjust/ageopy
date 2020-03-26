
import urllib
import json
import time



class Service(object):
    '''
        Started as a way to class out exporting from a map service.

        Using https://github.com/openaddresses/pyesridump as an example.
    '''

    def __init__(self, url):
        self.url = url
        

    def _get(self):
        pass




class MapService(Service):
    '''

        This Class is being setup as a way to get data from ESRI's ArcGIS Server
        
        ex:
            import ageopy.esri.server as ags
            mapservice = ags.MapService(url)
            oids = bikemap._get_layer_oids('0')
            
    '''
    def __init__(self, url):
        Service.__init__(self, url)


    def _query(self):
        query_url = self.url


    def _get_metadata(self):
        '''
            should probably be moved
            to Service definition
        '''
        data = {'f': 'pjson'}
        response = urllib.urlopen(self.url, urllib.urlencode(data))
        pjson = json.loads(response.read())
        return pjson


    def gulp_layer(self, layer_index):
        layer = MapLayer(layer_index)
        layer.gulp_layer()
        
        



        
class MapLayer():
    '''
        Do I pass self as the first argument when calling a function
        directly off of a clas (ie DataStore._storetype(self)

        Sample Call:
            import sys
            
            sys.path.append(r"\\path\to\ageopy")
            import ageopy.esri.server as ags
            url = 'http://mycity.houstontx.gov/cohgis/rest/services/PD/Bikeways_wm/MapServer/1'
            bikemap = ags.MapLayer(url)
            bikemap.gulp_layer(output_location=r'C:\bikehou', chunk_size=100)
    '''

    def __init__(self, url):
        self.url = url
        self.oids = MapLayer._get_layer_oids(self)
        self.out_srs = '4326'


    def _get_url_params(self):
        data = {}
        data['f'] = 'pjson'
        data['outSR'] = '4326'
        data['outFields'] = '*'
        return data


    def _get_layer_oids(self):
        data = {}
        data['f'] = 'pjson'
        data['where'] = '1=1'#'1%3D1'
        data['returnIdsOnly'] = 'true'
        query_url = self.url + '/query?'
        response = urllib.urlopen(query_url, urllib.urlencode(data))
        pjson = json.loads(response.read())
        return pjson


    def gulp_layer(self, chunk_size=None, pause_time=None, output_location=None):
        '''
            Should gulp_layer return a direct gulp of
            Server for ArcGIS or return a geojson object???
        '''
        MapLayer._gulp_layer_manager(self, chunk_size, output_location)


    def _gulp_layer_manager(self, chunk_size=None, output_location=None):
        if chunk_size is None:
            chunk_size = 25
        oidlist = self.oids['objectIds']
        chunked_oids = []
        for i in range(0, len(oidlist), chunk_size):
            chunk = map(int, oidlist[i:i + chunk_size])
            chunked_oids.append(chunk)
        result = MapLayer._gulp_layer_worker(self, chunked_oids, output_location)


    def _gulp_layer_worker(self, workload, output_location=None):
        features = []
        counter = 0
        for oid_chunk in workload:
            time.sleep(5)
            data = {}
            data['f'] = 'pjson'
            data['outFields'] = '*'
            data['returnGeometry'] = 'true'
            '''
            This looks to not work at 10.7
            data['Geometry'] = 'true'
            '''
            data['outSR'] = '4326'
            oidparam = ','.join(map(str, oid_chunk))
            data['objectIds'] = oidparam
            query_url = self.url + '/query?'
            response = urllib.urlopen(query_url, urllib.urlencode(data))
            pjson = response.read()
            MapLayer._write(self, pjson, output_location + "\\" + str(counter) + ".json")
            counter += 1
        return features


    def _write(self, result, src):
        with open(src, 'w') as data_file:
            data_file.write(str(result))



    



class GPService(Service):

    def __init__(self, path):
        DataElement.__init__(self, path)
        self.gdbobjectflatname = GDBElement._gdbobjectflatname(self)
        self.gdbrootpath, self.datastoretype = GDBElement._gdbrootpath(self)
        self.connectionpath = GDBElement._connectionpath(self)



