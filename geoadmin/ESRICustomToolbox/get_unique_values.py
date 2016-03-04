import gpFuncs as gpF
import traceback
import arcpy

def main():
    try:
        print "here"
        arcpy.AddMessage("here")
        table = arcpy.GetParameter(0)
        field = arcpy.GetParameter(1)
        unique_list = gpF.make_table_querylist_unique(table, field)
        gpF.eF.arcMessage(len(unique_list))
        for i in unique_list:
            gpF.eF.arcMessage(i)
    except:
        gpF.eF.arcMessage(traceback.format_exc())


if __name__ == "__main__":
    main()
