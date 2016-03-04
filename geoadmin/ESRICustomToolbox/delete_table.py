import sys
import os
import arcpy


def main():
    import dynseg_logging as logger
    path = "\\".join(os.path.realpath(__file__).split('\\')[:-1])
    log = logger.LogIt(path)
    report_name = arcpy.GetParameter(0)
    delete_table_name = assign_output(report_name)
    




def assign_output(report_name):
    path = "\\".join(os.path.realpath(__file__).split('\\')[:-1])
    outputdb = path + "\\" + "dynseg_user_schema.sde"
    rootname = outputdb + "\\background.DynSeg."
    if report_name == "HCA":
        return rootname + 'DYNSEG_HCA'
    elif report_name == "OperatingPressure":
        return rootname + 'DYNSEG_OperatingPressure'
    elif report_name == "Class":
        return rootname + 'DYNSEG_DOTCLASS'
    elif report_name == "PHMSA":
        return rootname + 'DYNSEG_PHMSA'
    elif report_name == "Accounting":
        return rootname + 'DYNSEG_Accounting'
    elif report_name == "test":
        return rootname + 'DYNSEG_TEST'
    elif report_name == "Compliance":
        return rootname + 'DYNSEG_COMPLIANCE'
    else:
        arcpy.AddMessage("Report type ***" + str(report_name) + "*** is not configured in the ***assign_output*** function." + os.linesep)
        raise Exception



if __name__ == "__main__":
    main()




