import os
import string
import sys
import traceback
import arcpy

c = r"\\aws0fspv1.boardwalk.corp\Shared$\AppData\GIS\Cloud\Software\Boardwalk\Code\QA\BoardwalkReportTools\report_data_refresh\QA_background_db_windows_auth.sde\background.gisprocess.DOTCLASS_V"
ci = "\\\\aws0fspv1.boardwalk.corp\\Shared$\\AppData\\GIS\\Cloud\\Software\\Boardwalk\\Code\\QA\\BoardwalkReportTools\\report_data_refresh\\QA_background_db_windows_auth.sde\\background.gisprocess.DOTCLASS_V"
#arcpy.AddMessage(arcpy.Exists(c))

#print os.path.basename(ci)


mylist = [u'\\\\aws0fspv1.boardwalk.corp\\Shared$\\AppData\\GIS\\Cloud\\Software\\Boardwalk\\Code\\QA\\BoardwalkReportTools\\report_data_refresh\\QA_background_db_windows_auth.sde\\background.gisprocess.DOTCLASS_V', u'\\\\aws0fspv1.boardwalk.corp\\Shared$\\AppData\\GIS\\Cloud\\Software\\Boardwalk\\Code\\QA\\BoardwalkReportTools\\report_data_refresh\\QA_background_db_windows_auth.sde\\background.gisprocess.COUNTYBOUNDARY_V', u'\\\\aws0fspv1.boardwalk.corp\\Shared$\\AppData\\GIS\\Cloud\\Software\\Boardwalk\\Code\\QA\\BoardwalkReportTools\\report_data_refresh\\QA_background_db_windows_auth.sde\\background.gisprocess.SUBSYSTEMRANGE_V']





for i in mylist:
    bl = i.split("\\")
    bl1 = "\\".join(bl)
    print bl1
    #arcpy.MakeQueryTable_management(i, "Class_DOTCLASS_V_VIEW", "USE_KEY_FIELDS", "background.gisprocess.DOTCLASS_V.DC_ObjectID", "", "")
