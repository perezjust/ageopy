import os
import webbrowser
import traceback



import ageopy.mapelement.amapdoc as amapdoc
from ageopy.mapelement.amapdoc import AMapDoc




def main():
    
    
    try:


        mxdpath = "CURRENT"
        mapdoc = AMapDoc(mxdpath)

        mapdoc.printtest()

        layers = mapdoc.get_layers()

        for i in layers:
            print i
            operator = "="
            value = "Value"
            field = "Source"
            mapdoc.set_layer_sql(i, value, field, operator)
        
        
    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()



if __name__ == "__main__":
    main()
