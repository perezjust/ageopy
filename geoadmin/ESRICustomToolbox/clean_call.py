import os


import clean_me# as cm


hotspots = r"\\l01923\c$\transfer\data\Comparisons.gdb\hotspots_jp"
hotspot_fieldlist = ["ROUTE", "SEGMENTNUM"]
hotspots = clean_me.fc_to_dict(hotspots, hotspot_fieldlist)


points = r"\\l01923\c$\transfer\data\Comparisons.gdb\points_jp"
points_fieldlist = ["ROUTE", "SEGMENTNUM"]
#points = cm.fc_to_dict(points, points_fieldlist)

clean_me.compare_fc_with_dict(hotspots, points, points_fieldlist)



##for key in hotspots:
##    print key
##    print hotspots[key]
##    for item in hotspots[key]:
##        print item

