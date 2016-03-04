import os
import webbrowser
import traceback



#Parameters
fgdb_path = arcpy.GetParameterAsText(0)

def main():
    try:

        
        
        from parse_contents import *
        '''
            This works because parse_contents.py is in the same folder as lws_data_check.py (this script)
        '''


        inproc = os.path.dirname(fgdb_path) + "\\" + "inproc.txt"
        start_proc(inproc)
        '''
            This has to do with writing the report file.
        '''


        try:
            
        
            fgdb_catalog = gpF.ESRI_DBBrowser(fgdb_path).build_db_catalog()
            '''
                gpF is part of a library that is imported in the parse_contents file above.
            '''

            
            report_name = "data_attribute_check.txt"
            duplicate_attribute_check(fgdb_catalog, fgdb_path, report_name)

            arcpy.AddMessage(" ")
            arcpy.AddMessage(" ")
            arcpy.AddMessage("The report was written to this file: ")
            arcpy.AddMessage(os.path.dirname(fgdb_path) + "\\" + report_name)
            arcpy.AddMessage(" ")
            arcpy.AddMessage(" ")
            webbrowser.open(os.path.dirname(fgdb_path) + "\\" + report_name)


        except:
            arcpy.AddMessage(traceback.format_exc())


        stop_proc(inproc)
        '''
            This has to do with writing the report file.
        '''
        
        
    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()



if __name__ == "__main__":
    main()
