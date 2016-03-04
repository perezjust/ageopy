import arcpy
import os
import string
import sys
import shutil
import traceback
import datetime
import time
import getpass
from os.path import join
from collections import defaultdict
import arceditor




import gpFuncs as gpF
from gpFuncs import *

logme = gpF.logIt(r"\\some\path")



def main():
    
    try:
        
        x = "This is dummy!  Parse_contents.py is now an imported library for other scripts."

        
    except:
        print traceback.format_exc()
        logme.logMessage(traceback.format_exc())









#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::





def check_vertices(fgdb_catalog):
    get_point_data_vertices(fgdb_catalog)
    layer_list = get_layers_from_mxd()
    for i in layer_list:
        get_vertices(i)
    



def get_layers_from_mxd(mxd_instance=None, dataframe=None):
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd, mxd.activeDataFrame.name)[0]
    if mxd_instance != None:
        mxd = arcpy.mapping.MapDocument(mxd_instance)
    if dataframe != None:
        df = arcpy.mapping.ListDataFrames(mxd, dataframe)[0]
    layer_list = arcpy.mapping.ListLayers(mxd, "", df)
    return layer_list



def get_vertices(fc):
    for i in arcpy.da.SearchCursor(fc, "*", "#", "#", True):
        for x in i:
            arcpy.AddMessage(x)
    
    

def get_point_data_vertices(fgdb_catalog):
    for fc in fgdb_catalog:
        if arcpy.Describe(fc).shapeType == "Point":
            get_vertices(fc)
    





#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::





def qa_report_write(fgdb_path, qa_type, line):
    inproc = os.path.dirname(fgdb_path) + "\\" + "inproc.txt"
    qa_file = os.path.dirname(fgdb_path) + "\\" + qa_type + ".txt"
    if os.path.exists(qa_file):
        logme.logMessage(os.path.getctime(qa_file))
        logme.logMessage(os.path.getctime(inproc))
        if float(os.path.getctime(qa_file)) < float(os.path.getctime(inproc)):
            os.remove(qa_file)
    with open(qa_file, "a") as wrt:
        wrt.write(line + "\r\n")


 
def start_proc(inproc):
    logme.logMessage("starting")
    if os.path.exists(inproc):
        os.remove(inproc)
    with open(inproc, "wb") as i:
        pass



def stop_proc(inproc):
    if os.path.exists(inproc):
        os.remove(inproc)




def update_sde(fgdb_catalog, dataset, fgdb_path):
    '''
        entry function for lws_data_to_sde ArcToolbox script tool
    '''
    missing_list = []
    created_list = []
    failed_list = []
    field_diffs_list = []
    sdepath = dataset + "\\" + "."
    for fgdb_fc in fgdb_catalog:
        sde_fc = str(sdepath) + str(os.path.basename(fgdb_fc))
        fl_gdb = gpF.featureLayer(fgdb_fc)
        if fl_gdb.count() > 0:
            try:
                if arcpy.Exists(sde_fc):
                    field_diffs_list.append(compare_fields(sde_fc, fgdb_fc))
                    arcpy.DeleteFeatures_management(sde_fc)
                    arcpy.Append_management(fgdb_fc, sde_fc, "NO_TEST")
                    print "Done: " + str(os.path.basename(fgdb_fc))
                    arcpy.AddMessage("Done: " + str(os.path.basename(fgdb_fc)))
                else:
                    missing_list.append(os.path.basename(fgdb_fc))
                    try:
                        gdb_shoehorn_sde(fgdb_fc, sde_fc, dataset)
                        created_list.append(os.path.basename(fgdb_fc))
                    except:
                        failed_list.append(fgdb_fc)
                        logme.logMessage(traceback.format_exc())
            except:
                print traceback.format_exc()
                arcpy.AddMessage(traceback.format_exc())
    update_sde_reporter(missing_list, fgdb_path, "Dataset doesnt't exist: ")
    update_sde_reporter(created_list, fgdb_path, "Dataset was created: ")
    update_sde_reporter(failed_list, fgdb_path, "Failed to Create: ")
    update_sde_reporter(field_diffs_list, fgdb_path, "Field: ")





def update_sde_reporter(inlist, fgdb_path, input_string):
    for i in inlist:
        qa_report_write(fgdb_path, "sde_update", input_string + str(i))




def delete_sdelayers_per_gdblayers(fgdb_catalog, dataset, delete_flag=None):
    sde_layers_deletes = []
    fgdb_layer_basenames = []
    error_list = []
    for fgdblayer in fgdb_catalog:
        fgdb_layer_basenames.append(os.path.basename(fgdblayer))
    arcpy.env.workspace = dataset
    for sde_fc in arcpy.ListFeatureClasses():
        non_sde_fc_name = sde_fc.split(".")[-1]
        if non_sde_fc_name not in fgdb_layer_basenames:
            sde_layers_deletes.append(dataset + "\\" + sde_fc)
            arcpy.AddMessage(sde_fc)
            if delete_flag == "true":
                try:
                    arcpy.Delete_management(dataset + "\\" + sde_fc)
                    arcpy.AddMessage("Deleted: " + sde_fc)
                except:
                    error_list.append(dataset + "\\" + sde_fc)
                    arcpy.AddMessage(traceback.format_exc())
    for erro in error_list:
        arcpy.AddMessage("Did not delete: " + str(erro))
    




def gdb_shoehorn_sde(fgdb_fc, sde_fc, dataset):
    if arcpy.Describe(fgdb_fc).shapeType == "Point":
        arcpy.CreateFeatureclass_management(dataset, os.path.basename(fgdb_fc), "POINT", fgdb_fc, "DISABLED", "DISABLED", dataset)
    elif arcpy.Describe(fgdb_fc).shapeType == "Polyline":
        arcpy.CreateFeatureclass_management(dataset, os.path.basename(fgdb_fc), "POLYLINE", fgdb_fc, "DISABLED", "DISABLED", dataset)
    arcpy.Append_management(fgdb_fc, sde_fc, "NO_TEST")




def compare_fields(existing, new):
    ignore_fields = ['OBJECTID', 'ID', 'IMG_ICON', 'Entity', 'Shape.len', 'Shape_Length']
    return_statement = []
    flds_comp_with = fieldNameList(existing)
    flds_type_comp_with = fieldTypeDict(existing)
    flds_comp_against = fieldNameList(new)
    flds_type_comp_against = fieldTypeDict(new)
    field_diff_list = []
    my_result = compare_fields_helper(flds_comp_with, flds_type_comp_with, flds_comp_against, flds_type_comp_against)
    for k,v in my_result.items():
        if v == 'semi_match' or v == 'under' or v == 'over':
            if k not in ignore_fields:
                field_diff_list.append(str(k) + "--" + str(v))
    if len(field_diff_list) > 0:
        return_statement.append(existing)
        return_statement.append(field_diff_list)
    return return_statement



def compare_fields_helper(inList1, inDictio1, inList2, inDictio2):
    match_dictio = {}
    for i in inList1:
        if i in inList2:
            '''
               At least partial match here
            '''
            if inDictio1[i] == inDictio2[i]:
                match_dictio[i] = "full_match"
            else:
                match_dictio["Existing: " + i + " - " + inDictio1[i] + " | New: " + i + " - " + inDictio2[i] ] = "semi_match"
        else:
            match_dictio[i] = "over"
    del i
    for j in inList2:
        if j not in inList1:
            match_dictio[j] = "under"
    return match_dictio



def fieldNameList(inTable):
    fldNameList = []
    for fi in arcpy.ListFields(inTable):
        fldNameList.append(fi.name)
    return fldNameList



def fieldTypeDict(inTable):
    dictio = {}
    for fi in arcpy.ListFields(inTable):
        dictio[fi.name] = fi.type
    return dictio



#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::




def get_sde_path(fgdb_path):
    sdepath = r"."
    sde_fc = sdepath + str(os.path.basename(fgdb_path))
    return sde_fc



def duplicate_attribute_check(fgdb_catalog, fgdb_path):
    pntno_list = defaultdict(list)
    shape_list = defaultdict(list)
    for fc_path in fgdb_catalog:
        try:
            fl = gpF.featureLayer(fc_path)
            if fl.count() > 0 and fl.shapeType == "Point":
                req_fields = ["POINT_NUMBER", "SHAPE@XY"]
                sc = arcpy.da.SearchCursor(fc_path, req_fields)
                for row in sc:
                    pntno_list[row[0]].append(os.path.basename(fc_path))
                    shape_list[row[1]].append(str(row[0]) + " - " + str(os.path.basename(fc_path)))
        except:
            print fc_path
            print traceback.format_exc()
    qa_report_write(fgdb_path, "data_attribute_check", "===========================================================================================")
    qa_report_write(fgdb_path, "data_attribute_check", "Duplicate Point Number -- [ Feature Classes with shared Point Number ]")
    qa_report_write(fgdb_path, "data_attribute_check", "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    for pntno_key in pntno_list:
        if len(pntno_list[pntno_key]) > 1:
            print str(pntno_key) + " -- " + str(pntno_list[pntno_key])
            qa_report_write(fgdb_path, "data_attribute_check", str(pntno_key) + " -- " + str(pntno_list[pntno_key]))
    qa_report_write(fgdb_path, "data_attribute_check", "===========================================================================================")
    qa_report_write(fgdb_path, "data_attribute_check", "Duplicate Geometries -- [ Point Number - Feature Classes with shared Geometries ]")
    qa_report_write(fgdb_path, "data_attribute_check", "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    for shape_key in shape_list:
        if len(shape_list[shape_key]) > 1:
            print str(shape_key) + " -- " + str(shape_list[shape_key])
            qa_report_write(fgdb_path, "data_attribute_check", str(shape_key) + " -- " + str(shape_list[shape_key]))



    
def build_field_list(fgdb_catalog):
    total_fields = defaultdict(list)
    for fc_path in fgdb_catalog:
        fl = gpF.featureLayer(fc_path)
        for fld in fl.fieldlist:
            total_fields[fld.name].append(os.path.basename(fc_path))
    for fld_key in total_fields:
        print str(fld_key) + " -- " + str(total_fields[fld_key])
    



def validate_fieldbook_attributes(fgdb_path, fgdb_catalog, lws_data_root_path, dataset):
    img_path = r"\\"
    fieldbooklist = get_gdb_fieldbooks(fgdb_catalog)
    img_dup_list = img_find_list(lws_data_root_path)
    fieldbook_clean_list = []
    missing_fieldbook_reports = dict()
    for fldbook_key in fieldbooklist:
        '''
            Cross referencing fieldbook values from gdb with actual pdfs received.
        '''
        if len(img_dup_list[fldbook_key]) > 0:
            '''
                These items will constitute a list that will be used
                to clean the field books so missing field books or
                mal-attributed values will not break web mapping pop-ups
            '''
            if os.path.exists(os.path.join(img_path, os.path.basename(img_dup_list[fldbook_key][0]))) == True:
                pass
            else:
                shutil.copyfile(img_dup_list[fldbook_key][0], os.path.join(img_path, os.path.basename(img_dup_list[fldbook_key][0])))
                print str(fldbook_key) + " has been saved to the web server."
                qa_report_write(fgdb_path, "fieldbook_check", str(fldbook_key) + " has been saved to the web server.") 
            fieldbook_clean_list.append(os.path.basename(img_dup_list[fldbook_key][0]))
        else:
            print "Missing Fieldbook -- " + str(fldbook_key)
            missing_fieldbook_reports[str(fldbook_key)] = str(fieldbooklist[fldbook_key][0])
            #qa_report_write(fgdb_path, "fieldbook_check", "Missing Fieldbook -- '" + str(fldbook_key) + "' | for this feature class: '" + str(fieldbooklist[fldbook_key][0]) + "'")
    missing_fieldbook_reporter(fgdb_path, missing_fieldbook_reports)
    clean_fieldbook_attributes(fgdb_catalog, fieldbook_clean_list, dataset)




def missing_fieldbook_reporter(fgdb_path, missing_fieldbook_reports):
    extension_list = [".pdf", ".PDF"]
    qa_report_write(fgdb_path, "fieldbook_check", "===========================================================================================")
    qa_report_write(fgdb_path, "fieldbook_check", "Fieldbook values missing the file extension")
    qa_report_write(fgdb_path, "fieldbook_check", "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    for i in missing_fieldbook_reports:
        if i[-4:] in extension_list:
            qa_report_write(fgdb_path, "fieldbook_check", "Missing Fieldbook -- '" + i + "' | for this feature class: '" + missing_fieldbook_reports[i] + "'")
    qa_report_write(fgdb_path, "fieldbook_check", "===========================================================================================")
    qa_report_write(fgdb_path, "fieldbook_check", "Fieldbook values not found in received fieldbook pdfs")
    qa_report_write(fgdb_path, "fieldbook_check", "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    for i in missing_fieldbook_reports:
        if i[-4:] not in extension_list:
            qa_report_write(fgdb_path, "fieldbook_check", "Missing Fieldbook -- '" + i + "' | for this feature class: '" + missing_fieldbook_reports[i] + "'")                                



def build_imgsource_field(sde_fc):
    fl = gpF.featureLayer(sde_fc)
    if "IMG_ICON" not in fl.getfieldlist(1):
        arcpy.AddField_management(fl.catalog_path, "IMG_ICON", "TEXT", "", "")




def clean_fieldbook_attribute_editsession(sde_fc, fieldbook_clean_list):
    print_list = []
    fl = gpF.featureLayer(sde_fc)
    if "IMG_ICON" in fl.getfieldlist(1):
        req_fields = ["FIELD_NOTES", "IMG_ICON"]
        sc = arcpy.da.UpdateCursor(sde_fc, req_fields)
        for row in sc:
            if row[0] not in fieldbook_clean_list:
                if row[0] not in print_list:
                    print_list.append(row[0])
                row[0] = "no_data.jpg"
                row[1] = "icon_no_data.jpg"
            else:
                row[1] = "icon_image.jpg"
            sc.updateRow(row)
    else:
        pass
    return print_list




def clean_fieldbook_attributes(fgdb_catalog, fieldbook_clean_list, dataset):
    sdepath = dataset + "\\" + ""
    print_list = []
    for fc_path in fgdb_catalog:
        if arcpy.Describe(fc_path).shapeType == "Point":
            sde_fc = str(sdepath) + str(os.path.basename(fc_path))
            try:
                build_imgsource_field(sde_fc)
                add_field_flag = 1
            except:
                print traceback.format_exc()
                arcpy.AddMessage(traceback.format_exc())
                print str(os.path.basename(sde_fc)) + " doesn't have the proper field for fieldbook popups"
            print_list.extend(clean_fieldbook_attribute_editsession(sde_fc, fieldbook_clean_list))
    print "========================================"
    arcpy.AddMessage("========================================")
    for pri in print_list:
        print " Set attribute to no_data.jpg for this fieldbook: " + str(pri)




def get_gdb_fieldbooks(fgdb_catalog):
    fieldbooklist = defaultdict(list)
    for fc_path in fgdb_catalog:
        try:
            fl = gpF.featureLayer(fc_path)
            if fl.shapeType == "Point":
                req_fields = ["FIELD_NOTES"]
                #req_fields = ["FIELD_NOTES", "FIELD_BOOK_REFERENCE", "MODIFIED_DATE", "MODIFIED_BY", "CREATED_DATE", "CREATED_BY", "PROCESSED_BY", "PROCESSED_DATE", "PROCESSED_NOTES", "SURVEY_DATE", "SURVEY_CREW"]
                sc = arcpy.da.SearchCursor(fc_path, req_fields)
                for row in sc:
                    if row[0] != None:
                        fieldbooklist[str(row[0])].append(os.path.basename(fc_path))
        except:
            print fc_path
            print traceback.format_exc()
            arcpy.AddMessage(traceback.format_exc())
    return fieldbooklist




def img_find_list(path):
    '''
        Use for inital image processing to find duplicates
    '''
    img_total_list = []
    img_unq_list =[]
    img_dup_list = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(path):
        for fi in filenames:
            if fi.endswith(".pdf") or fi.endswith(".PDF") or fi.endswith(".JPG") or fi.endswith(".jpg"):
                img_dup_list[fi].append(os.path.join(dirpath, fi))
    return img_dup_list



def find_none_values(fgdb_catalog):
    dataset_null_dict = {}
    for fc_path in fgdb_catalog:
        fc_null_attr_list = defaultdict(list)
        try:
            fl = gpF.featureLayer(fc_path)
            if fl.count() > 0:
                field_param_helper = fl.cursor_field_parameter_helper()
                sc = arcpy.da.SearchCursor(fc_path, field_param_helper)
                for row in sc:
                    field_count = 0
                    for field in row:
                        if row[field_count] == None:
                            fc_null_attr_list[field_param_helper[field_count]].append("None")
                        field_count += 1
                dataset_null_dict[os.path.basename] = fc_null_attr_list                    
        except:
            print fc_path
            print traceback.format_exc()
            arcpy.AddMessage(traceback.format_exc())
    print dataset_null_dict















if __name__ == "__main__":
    main()
