import os
import webbrowser
import traceback



#Parameters
fgdb_path = arcpy.GetParameterAsText(0)
dataset = arcpy.GetParameterAsText(1)

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
            '''
                gpF is part of a library that is imported in the parse_contents file above.
            '''

            
            lws_data_root_path = r"\\Some\Directory"
            report_name = "sde_update.txt"
            if dataset.split("\\")[-1] == "SomeSchema.SDE.SomeFeatureDataset":
                
                update_sde(fgdb_catalog, dataset, fgdb_path, report_name)
                
            else:
                arcpy.AddMessage("You did not choose the correct ArcSDE Feature DataSet: HERE IS DUMMY")



            arcpy.AddMessage(" ")
            arcpy.AddMessage(" ")
            arcpy.AddMessage("The report was written to this file: ")
            arcpy.AddMessage(os.path.dirname(fgdb_path) + "\\" + report_name)
            arcpy.AddMessage(" ")
            arcpy.AddMessage(" ")
            webbrowser.open(os.path.dirname(fgdb_path) + "\\" + report_name)

        except:
            
            arcpy.AddMessage(traceback.format_exc())
            print traceback.format_exc()


        stop_proc(inproc)
        '''
            This has to do with writing the report file.
        '''

        
        
    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()






if __name__ == "__main__":
    main()
