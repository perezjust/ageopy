import arcpy
import os
import sys
from collections import defaultdict

sys.path.append("\\".join(os.path.realpath(__file__).split('\\')[:-2]))
import esri.dataelement as de


class PODSElement(de.GDBElement):

    def __init__(self, path):
        de.GDBElement.__init__(self, path)
        self.fullschemaname = None
        if self.datastoretype == "sde":
            print self.datastoretype
            self.fullschemaname = PODSElement._fullschemaname(self)

    def _fullschemaname(self):
        pass



class PODSEventTable(PODSElement):

    def __init__(self, path, routeeventid=None):
        PODSElement.__init__(self, path)

        self.routeeventid = "RouteEventID"
        self.islinear = PODSEventTable._is_linear(self)
        if self.islinear == True:
            self.beginmeasure = "BeginMeasure"
            self.endmeasure = "EndMeasure"
            #self.measureranges = PODSEventTable._get_measure_ranges(self)

    def _is_linear(self):
        counter = 0
        if "BeginMeasure" in self.fieldnamelist:
            counter += 1
        if "EndMeasure" in self.fieldnamelist:
            counter += 1
        if counter == 2:
            return True
        else:
            return False

    def _get_measure_ranges(self):
        measuresdict = defaultdict(list)
        fldlist = [self.routeeventid, self.beginmeasure, self.endmeasure]
        for i in arcpy.da.SearchCursor(self.path, fldlist):
            measuresdict[i[0]].append([i[1], i[2]])
        return measuresdict

    def validate_measures(self):
        error_measures = []
        ridlist = []
##        with arcpy.da.SearchCursor(self.path, ["RouteEventID"]) as sc:
##            for i in sc:
##                ridlist.append(i[0])
        print self.connectionpath
        #sdeconn = arcpy.ArcSDESQLExecute(str(self.connectionpath))
        #sdeconn.execute("SELECT * FROM pods.GIS.StationSeries")#"select eventid from GIS.StationSeries")
        print ridlist
        


class PODSStationSeries(PODSElement):

    def __init__(self, path):
        PODSElement.__init__(self, path)
        self.eventid = "EventID"

    def _get_measure_ranges(self):
        measuresdict = defaultdict(list)
        fldlist = [self.eventid, self.beginmeasure, self.endmeasure]
        for i in arcpy.da.SearchCursor(self.PATH, fldlist):
            measuresdict[i[0]].append([i[1], i[2]])
        return measuresdict










    
        



    
