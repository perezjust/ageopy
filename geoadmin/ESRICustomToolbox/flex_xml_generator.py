import os
import webbrowser
import traceback



#Parameters
fgdb_path = arcpy.GetParameterAsText(0)

def main():
    try:

        
        
        from parse_contents import *
        '''
            gpF is part of a library that is imported in the parse_contents file above.
        '''

        inproc = os.path.dirname(fgdb_path) + "\\" + "inproc.txt"
        start_proc(inproc)
        '''
            This has to do with writing the report file.
        '''


        try:
            
        
            fgdb_catalog = gpF.ESRI_DBBrowser(fgdb_path).build_db_catalog()

            duplicate_attribute_check(fgdb_catalog, fgdb_path)
            #find_none_values(fgdb_catalog)


            arcpy.AddMessage(" ")
            arcpy.AddMessage(" ")
            arcpy.AddMessage("The report was written to this file: ")
            arcpy.AddMessage(os.path.dirname(fgdb_path) + "\\" + "data_attribute_check.txt")
            arcpy.AddMessage(" ")
            arcpy.AddMessage(" ")
            webbrowser.open(os.path.dirname(fgdb_path) + "\\" + "data_attribute_check.txt")


        except:
            arcpy.AddMessage(traceback.format_exc())


        stop_proc(inproc)
        
        
    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()






def build_sublayer():
    counter = 0
    while counter < 46:
        print '<sublayer id="' + str(counter) + '" popupconfig="popups/PopUp_Fieldbook.xml" />'
        counter += 1





def report_data():
    '''
        Use for inital image processing to find dups
    '''
    

    img_dup_list = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(path):
        for di in dirnames:
            print di




def build_xml_esearch():
    arcpy.env.workspace = r"Database Connections\dataconnection.sde\Some.SDE.Database"
    for fc_path in arcpy.ListFeatureClasses():
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print fc_path
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        fl = gpF.featureLayer(fc_path)
        for fld in fl.fieldlist:
            if "DATE" in str(fld.name):
                print '<field name="' + fld.name + '" gridfield="true" dateformat="MM/DD/YYYY" useutc="true"/>'
            else:
                print '<field name="' + fld.name + '" gridfield="true" gridfieldonly="true"/>'











if __name__ == "__main__":
    main()
