import os
import string
import sys
import shutil
import logging
import datetime
import traceback
from collections import defaultdict

import json
from pprint import pprint





import os
import sys
import exifread





def main():
    geo_dict = {}
    dirname = r"C:\Users\perezj\Desktop\exifheader\barlow"
    for fi in os.listdir(dirname):
        print fi + " -- " + str(buildgeo(os.path.join(dirname, fi)))[1:-1]
 
 
def _scrape_image(path_name):
    #path_name = "IMG_0674.JPG"
    # Open image file for reading (binary mode)
    f = open(path_name, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f)
    counter = 0
    for i in tags:
        print i
        if i == "GPS GPSLatitude":
            y = convertcoord(tags[i])
            counter += 1
        if i == "GPS GPSLongitude":
            x = convertcoord(tags[i])
            counter += 1
    if counter == 2:
        return [x,y]


def _convertcoord(coord):
    #print coord
    coord_list = str(coord)[1:-1].split(",")
    deg = coord_list[0]
    
    sec_raw = coord_list[2][1:].split("/")
    sec = float(sec_raw[0]) / float(sec_raw[1]) / 60
    #print "sec: " + str(sec)
    
    minutes_raw = float(coord_list[1][1:]) + sec
    minutes = minutes_raw / 60
    #print minutes
    
    return float(deg) + minutes




def query_esri_mapservice(url):
    pass




def get_url_params():
    data = {}
    data['f'] = 'pjson'
    data['outSR'] = '4326'
    data['outFields'] = '*'
    
    


def getGPServiceParameters(gpUrl):
    data = {'f': 'pjson'}
    gpServiceResponse = urllib.urlopen(gpUrl, urllib.urlencode(data))
    responseJson = json.loads(gpServiceResponse.read())
    return responseJson["parameters"][0]["choiceList"] 



def call_ags(report_type_name, taskUrl, log):
    submitUrl = taskUrl + "/submitJob"
    data = {'Report_Type': report_type_name, 'Run_Stored_Procedure': 'False', 'f': 'pjson'}
    submitResponse = urllib.urlopen(submitUrl, urllib.urlencode(data))
    responseJson = json.loads(submitResponse.read())
    if 'jobId' in responseJson:
            processResponse(responseJson, taskUrl)
            
    else:
            #No job was setup for request
            log.logMessage("No Job was setup for response")


def process_response(responseJson, taskUrl):
    print responseJson
    jobID = responseJson['jobId'] 
    status = responseJson['jobStatus']
    jobUrl = taskUrl + "/jobs/" + jobID
    print jobUrl
    counter = 0
    flag = 0
    while status == "esriJobSubmitted" or status == "esriJobExecuting":
            time.sleep(1)
            jobResponse = urllib.urlopen(jobUrl, "f=json")
            jobJson = json.loads(jobResponse.read())
            if 'jobStatus' in jobJson:
                    status = jobJson['jobStatus']
                    #print status
    if status == "esriJobSucceeded":
                    if 'results' in jobJson:
                            resultsUrl = jobUrl + "/results/"
                            resultsJson = jobJson['results']
                            print resultsJson
                            for paramName in resultsJson.keys():
                                    resultUrl = resultsUrl + paramName
                                    print resultUrl
                                    print paramName
                                    newlist = result_to_list(resultUrl)
    if status == "esriJobFailed":
                    if 'messages' in jobJson:
                            print jobJson['messages']




if __name__ == "__main__":
    main()
