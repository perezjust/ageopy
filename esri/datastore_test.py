import arcpy
import os
import string
import sys
import traceback
from os.path import join

import arcpy
import arceditor

import datastore

path = r"O:\AppData\GIS\Cloud\SDE files\GISCloudDev PODS.sde"
ds = datastore.GDBBrowser(path)
print ds.list_codeddomain_references("gnOperationalStatus")


