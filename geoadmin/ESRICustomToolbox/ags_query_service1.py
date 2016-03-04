# Queries the logs and writes statistics on map service activity during the past 24 hours

# For Http calls
import httplib, urllib, json

# For system tools
import sys, time

# For reading passwords without echoing
import getpass

#Defines the entry point into the script
def main(argv=None):

    logQueryURL = "/arcgis/admin/logs/query"
    startTime = int(round(time.time() * 1000))
    millisecondsToQuery = 86400000 # One day
    endTime = startTime - millisecondsToQuery
    logFilter = "{'services':'*','server':'*','machines':'*'}"

    params = urllib.urlencode({'level': 'FINE', 'startTime': startTime, 'endTime': endTime, 'filter':logFilter, 'token': '', 'f': 'json'})
    
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    serverName = "http://giscloudwebqa"
    serverPort = "6080"
    httpConn = httplib.HTTPConnection(serverName, serverPort)
    print httpConn
    httpConn.request("POST", logQueryURL, params, headers)
    response = httpConn.getresponse()
    

          
        

#A function that checks that the input JSON object
#  is not an error object.    
def assertJsonSuccess(data):
    obj = json.loads(data)
    if 'status' in obj and obj['status'] == "error":
        print "Error: JSON object returns an error. " + str(obj)
        return False
    else:
        return True
    
        
# Script start
if __name__ == "__main__":
    main()
