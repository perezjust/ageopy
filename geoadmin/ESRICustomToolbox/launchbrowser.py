import webbrowser
import arcpy
import traceback
import os




def main():
    try:

        url = "http://aws0isqv1:6080/arcgis/rest/services/"
        webbrowser.open(url)

    except:
        arcpy.AddMessage(traceback.format_exc())





if __name__ == "__main__":
    main()
