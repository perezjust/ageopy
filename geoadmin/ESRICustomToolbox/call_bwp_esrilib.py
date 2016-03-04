
import sys
import arcpy
import datetime

import sharedlibs_config
sys.path.insert(0, sharedlibs_config.BWP_ESRILIB_PATH)
import bwp_esrilib as bel


print bel.sde_item_create_date()
