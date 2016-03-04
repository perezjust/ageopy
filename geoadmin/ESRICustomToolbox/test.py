##import ageopy.mapelement.amapdoc as amapdoc
##from ageopy.mapelement.amapdoc import Amapdoc
##
##
##mxdpath = r""
##mapdoc = Amapdoc(mxdpath)
##
##mapdoc.printtest()
##
##layers = mapdoc.get_layers()
##
##for i in layers:
##    print i
##    value = "Value"
##    field = "Source"
##    mapdoc.set_layer_sql(i, value, field)
    

import


counter = 0
while counter == 0:
    try:
        arcpy = reload(arcpy)
        print "-"
        arcpy.ImportToolbox("C:/APPS/Python27/ArcGIS10.1/Lib/site-packages/boardwalk/esri/toolboxes/boardwalk.pyt")
    except:
        counter = 1
    
