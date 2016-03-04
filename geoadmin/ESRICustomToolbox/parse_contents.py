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
'''This works because gpFuncs.py is in the same folder as parse_contents.py'''



logme = gpF.logIt(r"\\SomeDir\Logs\parse_contents")



def main():
    
    try:
        
        x = "This is a placeholder!  Parse_contents.py is now an imported library for other scripts."

        
    except:
        print traceback.format_exc()
        logme.logMessage(traceback.format_exc())









#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#::::::::::::::::::::::::::    LINE WORK VERTEX CHECKING   :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#



def check_vertices(fgdb_catalog, accuracy, attribute_new_linework=None, new_linework_folder=None):
    point_vertex_dict = get_point_data_vertices(fgdb_catalog, accuracy)
    layer_list = get_layers_from_mxd()
    for i in layer_list:
        if i.supports("dataSource"):
            if arcpy.Describe(i.dataSource).shapeType == "Polyline":
                check_polyline_data_vertices(i, point_vertex_dict, accuracy, attribute_new_linework, new_linework_folder)



def get_layers_from_mxd(mxd_instance=None, dataframe=None):
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd, mxd.activeDataFrame.name)[0]
    if mxd_instance != None:
        mxd = arcpy.mapping.MapDocument(mxd_instance)
    if dataframe != None:
        df = arcpy.mapping.ListDataFrames(mxd, dataframe)[0]
    layer_list = arcpy.mapping.ListLayers(mxd, "", df)
    return layer_list



def build_new_linework(layer, point_vertex_dict, accuracy, new_linework_folder):
    arcpy.env.overwriteOutput = True
    build_folder = os.path.join(new_linework_folder, "linework")
    if not os.path.exists(build_folder):
        os.mkdir(build_folder)
    new_linework = os.path.join(build_folder, os.path.basename(layer.dataSource))
    arcpy.CopyFeatures_management(layer, new_linework)
    attribute_transfer_dict = check_polyline_data_vertices2(new_linework, point_vertex_dict, accuracy)
    



def check_polyline_data_vertices2(layer, point_vertex_dict, accuracy, attribute_new_linework=None, new_linework_folder=None):
    '''

        In Development...tools are using check_polyline_data_vertices function.  What needs to done to
        get this to transfer attributes is that the get_point_data_vertices needs to be adjusted to hold the
        point data attributes total...currently it just has the coordinates as the function name implies.

        The function get_point_data_vertices already has the full attribute data it just needs to include it in
        the returned results.

    '''
    arcpy.AddMessage("=============================================================")
    arcpy.AddMessage(layer)
    arcpy.AddMessage("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    fL = gpF.featureLayer(layer)
    fL_cursor_dict = fL.cursor_to_dicts2()
    vertex_dict = defaultdict(list)
    for i in fL_cursor_dict:
        '''
            i is a record in a data source.  cursor_to_dicts2() builds a dictionary of the entire data source's attribute table.
            We then step through each record...which is i.
        '''
        vertex_object = i["SHAPE@"]["coordinates"]

        attribute_transfer_dict = {}
        
        fc_found_count = 0
        fc_missed_count = 0
        fc_total_vertex_count = 0
        for j in vertex_object[0]:
            '''
                Here we are looking to see if the vertex j is in the vertices list (point_vertex_dict).
            '''
            floated_vertex = float_coordinates(j, accuracy)
            '''
                floated_vertex is a string representation of a vertex in the format "(x, y)"
                we want to see if the string matches any vertex strings in our dictionary of point data vertices
                we also are formatting the value to see if it matches 
            '''
            if len(point_vertex_dict[floated_vertex]) > 0:
                #arcpy.AddMessage(str(point_vertex_dict[float_coordinates(j, accuracy)]))
                fc_found_count +=1
                arcpy.AddMessage(point_vertex_dict[floated_vertex])
                attribute_transfer_dict.update(point_vertex_dict[floated_vertex])
            else:
                fc_missed_count += 1
            fc_total_vertex_count += 1
        if attribute_new_linework == "true":
            build_new_linework(vertex_object[0], point_vertex_dict, accuracy, new_linework_folder)
        fc_stat_list = "Total Vertices:" + str(fc_total_vertex_count) + " Matched Vertices:" + str(fc_found_count) + " Missed Vertices:--" + str(fc_missed_count)
        if "OBJECTID" not in i:
            arcpy.AddMessage( "FID:" + str(i["FID"]) + "-> " + str(fc_stat_list))
        else:
            arcpy.AddMessage( "OBJECTID:" + str(i["OBJECTID"]) + "-> " + str(fc_stat_list))



def check_polyline_data_vertices(layer, point_vertex_dict, accuracy):
    arcpy.AddMessage("=============================================================")
    arcpy.AddMessage(layer)
    arcpy.AddMessage("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    fL = gpF.featureLayer(layer)
    fL_cursor_dict = fL.cursor_to_dicts2()
    vertex_dict = defaultdict(list)
    for i in fL_cursor_dict:
        '''
            i is a record in a data source.  cursor_to_dicts2() builds a dictionary of the entire data source's attribute table.
            We then step through each record...which is i.
        '''
        vertex_object = i["SHAPE@"]["coordinates"]
        fc_found_count = 0
        fc_missed_count = 0
        fc_total_vertex_count = 0
        for j in vertex_object[0]:
            '''
                Here we are looking to see if the vertex j is in the vertices list (point_vertex_dict).
            '''
            floated_vertex = float_coordinates(j, accuracy)
            '''
                floated_vertex is a string representation of a vertex in the format "(x, y)"
                we want to see if the string matches any vertex strings in our dictionary of point data vertices
                we also are formatting the value to see if it matches
            '''
            if len(point_vertex_dict[floated_vertex]) > 0:
                #arcpy.AddMessage(str(point_vertex_dict[float_coordinates(j, accuracy)]))
                fc_found_count +=1
            else:
                fc_missed_count += 1
                arcpy.AddMessage(floated_vertex)
            fc_total_vertex_count += 1
        fc_stat_list = "Total Vertices:" + str(fc_total_vertex_count) + " Matched Vertices:" + str(fc_found_count) + " Missed Vertices:--" + str(fc_missed_count)
        if "OBJECTID" not in i:
            arcpy.AddMessage( "FID:" + str(i["FID"]) + "-> " + str(fc_stat_list))
        else:
            arcpy.AddMessage( "OBJECTID:" + str(i["OBJECTID"]) + "-> " + str(fc_stat_list))



def get_point_data_vertices(fgdb_catalog, accuracy):
    vertex_dict = defaultdict(list)
    for fc in fgdb_catalog:
        if arcpy.Describe(fc).shapeType == "Point":
            fL = gpF.featureLayer(fc)
            fL_cursor_dict = fL.cursor_to_dicts2()
            for i in fL_cursor_dict:
                vertex_object = i["SHAPE@"]["coordinates"]
                vertex_dict[float_coordinates(vertex_object, accuracy)].append(os.path.basename(str(fc)))
    return vertex_dict



def float_coordinates(coords_object, accuracy):
    coords_floated = "(" + "{0:.{1}f}".format(coords_object[0],accuracy) + ", " + "{0:.{1}f}".format(coords_object[1],accuracy) + ")"
    return coords_floated




#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#::::::::::::::::::::::::::    REPORT CREATION FOR VARIOUS QA CYCLES   :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#




def qa_report_write(fgdb_path, report_name, line):
    inproc = os.path.dirname(fgdb_path) + "\\" + "inproc.txt"
    qa_file = os.path.dirname(fgdb_path) + "\\" + report_name
    if os.path.exists(report_name):
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



#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#::::::::::::::::::::::::::    UPDATING SDE WITH GDB DATA   ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#


def update_sde(fgdb_catalog, dataset, fgdb_path, report_name):
    '''
        entry function for lws_data_to_sde ArcToolbox script tool
    '''
    missing_list = []
    created_list = []
    failed_list = []
    field_diffs_list = []
    sdepath = dataset + "\\" + "DBNAME.SDE."
    for fgdb_fc in fgdb_catalog:
        sde_fc = str(sdepath) + str(os.path.basename(fgdb_fc))
        fl_gdb = gpF.featureLayer(fgdb_fc)
        if fl_gdb.count() > 0:
            try:
                if arcpy.Exists(sde_fc):
                    field_diffs_list.append(compare_fields(sde_fc, fgdb_fc))
                    arcpy.DeleteFeatures_management(sde_fc)
                    arcpy.Append_management(fgdb_fc, sde_fc, "NO_TEST")
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
    update_sde_reporter(missing_list, fgdb_path, "Dataset doesnt't exist: ", report_name)
    update_sde_reporter(created_list, fgdb_path, "Dataset was created: ", report_name)
    update_sde_reporter(failed_list, fgdb_path, "Failed to Create: ", report_name)

    new_field_diffs_list = clean_report_list(field_diffs_list)
    update_sde_reporter(new_field_diffs_list, fgdb_path, "Schema Differences: ", report_name)




def clean_report_list(report_list):
    '''Help clean up empty reporting objects for a cleaner report'''
    new_list = []
    for i in report_list:
        if len(i) > 0:
            new_list.append(i)
    return new_list




def update_sde_reporter(inlist, fgdb_path, input_string, report_name):
    for i in inlist:
        qa_report_write(fgdb_path, report_name, input_string + str(i))




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



#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#::::::::::::::::::::::::::    ATTRIBUTE CHECKING   ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#




def get_sde_path(fgdb_path):
    sdepath = r"X:\py_updater_script.sde\DBNAME.SDE.FeatureDataSetName\DBNAME.SDE."
    sde_fc = sdepath + str(os.path.basename(fgdb_path))
    return sde_fc



def duplicate_attribute_check(fgdb_catalog, fgdb_path, report_name):
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
    attribute_qa_writer(fgdb_path, report_name, "Duplicate Point Number -- [ Feature Classes with shared Point Number ]", pntno_list)
    attribute_qa_writer(fgdb_path, report_name, "Duplicate Geometries -- [ Point Number - Feature Classes with shared Geometries ]", shape_list)



def attribute_qa_writer(fgdb_path, report_name, title, report_list):
    qa_report_write(fgdb_path, report_name, "===========================================================================================")
    qa_report_write(fgdb_path, report_name, title)
    qa_report_write(fgdb_path, report_name, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    if len(report_list) == 0:
        arcpy.AddMessage("hereee")
        qa_report_write(fgdb_path, report_name, "zero items to report")
        arcpy.AddMessage("here")
    else:
        for report_key in report_list:
            if len(report_list[report_key]) > 1:
                qa_report_write(fgdb_path, report_name, str(report_key) + " -- " + str(report_list[report_key]))



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




#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#::::::::::::::::::::::::::    FIELDBOOK CHECKING -- below  ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#



    
def build_field_list(fgdb_catalog):
    total_fields = defaultdict(list)
    for fc_path in fgdb_catalog:
        fl = gpF.featureLayer(fc_path)
        for fld in fl.fieldlist:
            total_fields[fld.name].append(os.path.basename(fc_path))
    for fld_key in total_fields:
        print str(fld_key) + " -- " + str(total_fields[fld_key])
    



def validate_fieldbook_attributes(fgdb_path, fgdb_catalog, lws_data_root_path, dataset, report_name):
    img_path = r"\\someserver\asbuilt_links"
    fieldbooklist = get_gdb_fieldbooks(fgdb_catalog)
    fldbook_fileserver_list = img_find_list(lws_data_root_path)
    fieldbook_clean_list = []
    missing_fieldbook_reports = dict()
    for fldbook_key in fieldbooklist:
        '''
            Cross referencing fieldbook values from gdb with actual pdfs received.
        '''
        if len(fldbook_fileserver_list[fldbook_key[:-4] + ".pdf"]) > 0 or len(fldbook_fileserver_list[fldbook_key[:-4] + ".PDF"]) > 0:
            pdfsavebasename = ""
            pdfsourcepath = ""
            '''
                if/elif below is finding
            '''
            if len(fldbook_fileserver_list[fldbook_key[:-4] + ".pdf"]) > 0:
                pdfsourcepath = fldbook_fileserver_list[fldbook_key[:-4] + ".pdf"][0]
            elif len(fldbook_fileserver_list[fldbook_key[:-4] + ".PDF"]) > 0:
                pdfsourcepath = fldbook_fileserver_list[fldbook_key[:-4] + ".PDF"][0]
            else:
                arcpy.AddMessage("Something bad happened! " + str(fldbook_fileserver_list[fldbook_key][0]))
                return
            if os.path.exists(os.path.join(img_path, os.path.basename(pdfsourcepath))) == True:
                pass
                #here it exists on file server, web server and attribute table
            else:
                #doesn't exist on web server then saves on web server
                shutil.copyfile(pdfsourcepath, os.path.join(img_path, os.path.basename(pdfsourcepath)))
                qa_report_write(fgdb_path, report_name, str(fldbook_key) + " has been saved to the web server.") 
            fieldbook_clean_list.append(fldbook_key)
        else:
            missing_fieldbook_reports[str(fldbook_key)] = str(fieldbooklist[fldbook_key][0])
    missing_fieldbook_reporter(fgdb_path, missing_fieldbook_reports, report_name)
    clean_fieldbook_attributes(fgdb_catalog, fieldbook_clean_list, dataset)




def missing_fieldbook_reporter(fgdb_path, missing_fieldbook_reports, report_name):
    extension_list = [".pdf", ".PDF"]
    qa_report_write(fgdb_path, report_name, "===========================================================================================")
    qa_report_write(fgdb_path, report_name, "Fieldbook values missing the file extension")
    qa_report_write(fgdb_path, report_name, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    for i in missing_fieldbook_reports:
        if i[-4:] not in extension_list:
            qa_report_write(fgdb_path, report_name, "Missing Fieldbook -- '" + i + "' | for this feature class: '" + missing_fieldbook_reports[i] + "'")
    qa_report_write(fgdb_path, report_name, "===========================================================================================")
    qa_report_write(fgdb_path, report_name, "Fieldbook values not found in received fieldbook pdfs")
    qa_report_write(fgdb_path, report_name, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    for i in missing_fieldbook_reports:
        if i[-4:] in extension_list:
            qa_report_write(fgdb_path, report_name, "Missing Fieldbook -- '" + i + "' | for this feature class: '" + missing_fieldbook_reports[i] + "'")                                



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
    sdepath = dataset + "\\" + "DBNAME.SDE."
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
                '''
                    Edited the line above and saved it pre-edit version below:
                    img_dup_list[fi].append(os.path.join(dirpath, fi))
                '''
    return img_dup_list





if __name__ == "__main__":
    main()
