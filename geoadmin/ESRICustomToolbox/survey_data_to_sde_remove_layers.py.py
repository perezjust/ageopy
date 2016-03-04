import os
import webbrowser
import traceback



#Parameters
fgdb_path = arcpy.GetParameterAsText(0)
dataset = arcpy.GetParameterAsText(1)
delete_flag = arcpy.GetParameterAsText(2)

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
            if dataset.split("\\")[-1] == "SomeSchema.SDE.SomeDataset":
                
                delete_sdelayers_per_gdblayers(fgdb_catalog, dataset, delete_flag)
                
            else:
                arcpy.AddMessage("You did not choose the correct ArcSDE Feature DataSet: HERE")


            arcpy.AddMessage(" ")
            arcpy.AddMessage(" ")
            arcpy.AddMessage("The report was written to this file: ")
            arcpy.AddMessage(os.path.dirname(fgdb_path) + "\\" + "sde_update.txt")
            arcpy.AddMessage(" ")
            arcpy.AddMessage(" ")
            #webbrowser.open(os.path.dirname(fgdb_path) + "\\" + "sde_update.txt")

        except:
            
            arcpy.AddMessage(traceback.format_exc())
            print traceback.format_exc()


        stop_proc(inproc)

        
        
    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()






if __name__ == "__main__":
    main()
