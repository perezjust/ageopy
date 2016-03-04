import os
import sys
import arcpy
from collections import defaultdict







def main():
    print "hidden inside clean_me.main() so you cant me."


def compare_fc_with_dict(fc_dict, fc_path, fc_fieldlist):
    ucur = arcpy.da.UpdateCursor(fc_path, fc_fieldlist)

    for row in ucur:
        """
            row[0] is item one in your fc_fieldlist (ie "ROUTE")
            row[1] is "SEGMENTNUM"

            If hotspots' route val in points >> keep points
            
        """
        if row[0] not in fc_dict and row[1] not in fc_dict[row[0]]:
            print row[0]
            ucur.deleteRow()
            """
                NOTE:
                fc_dict[row[0]] is getting your list for each route

                len(fc_dict[row[0]]) equals how many times that route showed up in points table

                
                if segmentnum is in list of hotspots segmentnum's list
                then the record stays in points
            """
    


def fc_to_dict(fc_path, fieldlist):
    route_dict_has_segments = defaultdict(list)
    sc = arcpy.da.SearchCursor(fc_path, fieldlist)
    counter = 0
    for row in sc:
        route_dict_has_segments[row[0]].append(row[1])

    return route_dict_has_segments
    

if __name__ == "__main__":
    main()




