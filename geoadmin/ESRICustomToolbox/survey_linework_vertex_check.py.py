import os
import webbrowser
import traceback



#Parameters
accuracy = arcpy.GetParameterAsText(0)
fgdb_catalog = arcpy.GetParameter(1)
'''Notice the GetParameter vs GetParameterAsText'''

def main():
    try:

        
        
        from parse_contents import *
        '''
            This works because parse_contents.py is in the same folder as lws_linework_vertex_check.py (this script)
        '''


        try:
            
        
            #fgdb_catalog = gpF.ESRI_DBBrowser(fgdb_path).build_db_catalog()
            '''
                gpF is part of a library that is imported in the parse_contents file above.
            '''

            check_vertices(fgdb_catalog, accuracy)



        except:
            arcpy.AddMessage(traceback.format_exc())
        
        
    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()



if __name__ == "__main__":
    main()
