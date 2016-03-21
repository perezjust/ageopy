import arcpy
import os
import string
import sys
import traceback
from os.path import join

import arcpy
import arceditor

import dataelement




class DataStore(object):
    
    def __init__(self, path):
        self.path = path
        self.storetype = DataStore._storetype(self)

    def _storetype(self):
        if ".sde" in self.path:
            return "sde"
        elif ".gdb" in self.path:
            return "gdb"
        else:
            return "folder"

    def _storetype2(self):
        minus1item = self.path.split("\\")[-1]
        minus2item = self.path.split("\\")[-2]
        minus3item = self.path.split("\\")[-3]




class DataStoreBrowser(DataStore):

    def __init__(self, path):
        DataStore.__init__(self, path)
  



class GDBBrowser(DataStoreBrowser):
    '''
        Build esri gdb catalog of all gdb ArcCatalog objects
    '''

    def __init__(self, path, datatypes=None):
        DataStoreBrowser.__init__(self, path)
        self.fclist = GDBBrowser._fclist(self)
        self.tablelist = GDBBrowser._tablelist(self)
        self.codeddomainlist = GDBBrowser._codeddomainlist(self)

    def _codeddomainlist(self, shortname=None):
        print "...Listing Coded Domains for " + self.path
        cdlist = []
        for i in arcpy.da.ListDomains(self.path):
            cdlist.append(i.name)
        return cdlist

    def list_codeddomain_references(self, domainname):
        for i in GDBBrowser._catalog(self):
            gdbelement = dataelement.GDBElement(i)
            if domainname in gdbelement._list_codeddomains():
                print domainname

    def _catalog(self):
        cataloglist = []
        for dirpath, dirnames, filenames in arcpy.da.Walk(self.path):
            for filename in filenames:
                cataloglist.append(os.path.join(dirpath, filename))
        return cataloglist

    def exporttofolder(self, folder, fclist=None):
        if not os.path.exists(folder):
            os.mkdir(folder)
        if not os.path.exists(join(folder, self.dbname)):
            os.mkdir(join(folder, self.dbname))
        if fclist is None:
            fclist = self.build_db_catalog()
        print fclist
        for fc in fclist:
            fcname = arcpy.Describe(fc).name.split(".")[-1]
            print fcname
            destination = ""
            #the feature class does not reside in a feature dataset
            if os.path.dirname(fc) == os.path.basename(self.path):
                destination = join(folder, self.dbname)
            else:
                datasetname = arcpy.Describe(os.path.dirname(fc)).name.split(".")[-1]
                destination = join(folder, self.dbname, datasetname)
            if not os.path.exists(destination):
                os.mkdir(destination)
            print destination
            arcpy.CopyFeatures_management(fc, join(destination, fcname))

    def _fclist(self):
        '''
            Renamed to build_fc_list.  Testing deprecation process.
        '''
        print "...Listing Feature Classes for " + self.path
        featureclasslist = []
        arcpy.env.workspace = self.path
        for fc in arcpy.ListFeatureClasses():
            featureclasslist.append(join(self.path, fc))
        for ds in arcpy.ListDatasets():
            arcpy.env.workspace = join(self.path, ds)
            for fc in arcpy.ListFeatureClasses():
                featureclasslist.append(join(join(self.path, ds), fc))
        return featureclasslist

    def _tablelist(self):
        tablelist = []
        arcpy.env.workspace = self.path
        for table in arcpy.ListTables():
            tablelist.append(join(self.path, table))
        return tablelist

    def _compare_domains(self, datastorecomp):
        print "*" * 23
        print "Domain not in DB: " + datastorecomp.PATH
        print "- - " * 6
        for i in set(self.codeddomainlist) - set(datastorecomp.codeddomainlist):
            print i
        print "*" * 23
        print "Domain not in DB: " + self.path
        print "- - " * 6
        for j in set(datastorecomp.codeddomainlist) - set(self.codeddomainlist):
            print j

    def _compare_featureclasslist(self, datastorecomp):
        self_fclist = []
        comp_fclist = []
        for fc_path in self.fclist:
            self_fclist.append(dataelement.GDBElement(fc_path).gdbobjectflatname)
        for fc_path_comp in datastorecomp.fclist:
            comp_fclist.append(dataelement.GDBElement(fc_path_comp).gdbobjectflatname)
        print "*" * 23
        print "Feature Classes not in DB: " + datastorecomp.path
        print "- - " * 6
        for i in set(self_fclist) - set(comp_fclist):
            print i
        print "*" * 23
        print "Feature Classes not in DB: " + self.path
        print "- - " * 6
        for j in set(comp_fclist) - set(self_fclist):
            print j

    def compare_schema(self, datastore, dataypes=None):
        """
            Compares the schema objects specified in the datatypes parameter.
            
            Parameters:
            datastore: string
                The top-level datastore that will be used.
            datatypes: string | list | tuple
                Keywords(s) representing the desired datatype objects to compare. A
                single datatype can be expressed as a string, otherwise use a list
                or tuple.
        """
        datastorecomp = GDBBrowser(datastore)
        self._compare_featureclasslist(datastorecomp)
        self._compare_domains(datastorecomp)




class FolderBrowser(DataStoreBrowser):

    def __init__(self, path):
        DataStoreBrowser.__init__(self, path)
        #this does nothing right now
        desc = arcpy.Describe(path)
        workspacetype = desc.workspaceType
        if workspacetype == "FileSystem":
            print "File System"

    def build_fs_catalog(self):
        featureclasslist = []
        folder = str(self.path)
        arcpy.env.workspace = self.path
        for root,dir,files in os.walk(folder):
            filelist = [ os.path.join(root,fi) for fi in files if fi.endswith(".shp")]
            for f in filelist:
                    featureclasslist.append(f)
        return featureclasslist




















