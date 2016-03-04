import webbrowser
import arcpy
import traceback
import os
import json




def main():
    try:



##        try:
##            
##            configFile = path + "\\dynseg.config"
##            json_data=open(configFile).read()
##            arcpy.AddMessage(json_data)
##            config = json.loads(json_data)
##            log.logMessage(config)
##            
##        except Exception,ErrorDesc:
##            raise Exception("Configuration file error: " + str(ErrorDesc))

        

        input_fc = arcpy.GetParameter(0)
        input_flds = arcpy.GetParameter(1)
        json_file = arcpy.GetParameter(2)
        func1(input_fc, input_flds)

    except:
        arcpy.AddMessage(traceback.format_exc())



def func1(input_fc, input_flds):
    fld_list = []
    for i in input_flds:
        fld_list.append(str(i))
    fld_dict = {}
    fld_dict[input_fc.dataSource] = fld_list
    data_string = json.dumps(fld_dict)
    
    arcpy.AddMessage(data_string)




if __name__ == "__main__":
    main()
