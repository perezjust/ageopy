import urllib
import json
import time
import arcpy
import traceback
import os
import datetime
import imp


arcpy.env.overwriteOutput = True



def main():
    environment = getEnvironment()
    homepath = os.path.dirname(__file__)
    main_config_path = homepath + "\\config_main.config"
    log = getLogger(environment, getConfig(environment, main_config_path))
    try:
        log.logMessage("LOG HEADER: DynSeg Scheduled Task Logging")
        taskUrl = getTaskURL(environment)
        report_choice_list = getGPServiceParameters(taskUrl)

        
        for report_choice in report_choice_list:
            try:
                if report_choice != "test":
                    print report_choice
                    call_ags(report_choice, taskUrl, log)
            except:
                log.logMessage(traceback.format_exc())
        

    except:
        log.logMessage(traceback.format_exc())



def getGPServiceParameters(gpUrl):
    data = {'f': 'pjson'}
    gpServiceResponse = urllib.urlopen(gpUrl, urllib.urlencode(data))
    responseJson = json.loads(gpServiceResponse.read())
    return responseJson["parameters"][0]["choiceList"]


def getConfig(environment, configpath):
    print configpath
    with open(configpath, "r") as file_reader:
        config_dict = json.loads(file_reader.read())
    return config_dict


def getLogger(environment, config_dict):
    giscommon = config_dict["GISCOMMON"]
    logmodule = config_dict["LOGGINGMODULE"]
    logpath = config_dict["LOGGINGPATH"]
    full_logmod_path = os.path.join(giscommon, environment, logmodule)
    module_name = str(logmodule)[:-3]
    logger = imp.load_source(module_name, full_logmod_path)
    log = logger.LogIt(logpath)
    return log


def getTaskURL(environment):
	taksURL = ""
    return taskURL


def getEnvironment():
    compname = os.getenv('COMPUTERNAME')
    if compname == "":
		envt = ""
        
    return envt


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


def processResponse(responseJson, taskUrl):
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



def result_to_list(resultUrl):
    resultResponse = urllib.urlopen(resultUrl, "f=json")
    resultJson = json.loads(resultResponse.read())
    result_list = resultJson["value"].split(",")
    return result_list






if __name__ == "__main__":
    main()
