import urllib
import json
import time
import arcpy
import traceback


arcpy.env.overwriteOutput = True


def main():
    try:
        

        taskUrl = "http://giscloudwebqa:6080/arcgis/rest/services/AGSReportDomainUsage/GPServer/AGSReportDomainUsage"
        submitUrl = taskUrl + "/submitJob"

        data = {'f': 'pjson'}
        
        submitResponse = urllib.urlopen(submitUrl, urllib.urlencode(data))
        submitJson = json.loads(submitResponse.read()) 
        if 'jobId' in submitJson:  
            jobID = submitJson['jobId']        
            status = submitJson['jobStatus']        
            jobUrl = taskUrl + "/jobs/" + jobID
            print jobUrl
            counter = 0
            flag = 0
            while status == "esriJobSubmitted" or status == "esriJobExecuting":
                print status
                counter += 1
                print "checking to see if job is completed..." + str(counter)
                time.sleep(1)
                
                jobResponse = urllib.urlopen(jobUrl, "f=json")     
                jobJson = json.loads(jobResponse.read())
         
                if 'jobStatus' in jobJson:
                    status = jobJson['jobStatus']

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



    except:
        print traceback.format_exc()
        arcpy.AddMessage(traceback.format_exc())



def result_to_list(resultUrl):
    resultResponse = urllib.urlopen(resultUrl, "f=json")
    resultJson = json.loads(resultResponse.read())
    result_list = resultJson["value"].split(",")
    return result_list






if __name__ == "__main__":
    main()
