import os
import webbrowser
import traceback




#Parameters
fgdb_path = arcpy.GetParameterAsText(0)
lws_data_root_path = arcpy.GetParameterAsText(1)
dataset = arcpy.GetParameterAsText(2)

def main():

    from parse_contents import *
    '''
        parse_contents.py is the library for this script tool and is in the same directory as this script 
    '''
    
    inproc = os.path.dirname(fgdb_path) + "\\" + "inproc.txt"
    start_proc(inproc)
    '''
        This has to do with writing the report file.
    '''
    
    try:
        


        fgdb_catalog = gpF.ESRI_DBBrowser(fgdb_path).build_db_catalog()
        report_name = "fieldbook_check.txt"
        if dataset.split("\\")[-1] == "SomeSchema.SDE.SomeDataset":
            
            
            validate_fieldbook_attributes(fgdb_path, fgdb_catalog, lws_data_root_path, dataset, report_name)

            
            arcpy.AddMessage(" ")
            arcpy.AddMessage(" ")
            arcpy.AddMessage("The report was written to this file: ")
            arcpy.AddMessage(os.path.dirname(fgdb_path) + "\\" + report_name)
            arcpy.AddMessage(" ")
            arcpy.AddMessage(" ")
            webbrowser.open(os.path.dirname(fgdb_path) + "\\" + report_name)
            
            
        else:
            arcpy.AddMessage("You did not choose the correct ArcSDE Feature DataSet: HERE")
        
        
    except:
        arcpy.AddMessage(traceback.format_exc())
        print traceback.format_exc()

    stop_proc(inproc)

    







if __name__ == "__main__":
    main()
