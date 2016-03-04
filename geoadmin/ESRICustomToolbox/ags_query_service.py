# Queries the logs and writes statistics on map service activity during the past 24 hours

# For Http calls
import httplib, urllib, json

# For system tools
import sys, time

# For reading passwords without echoing
import getpass

#Defines the entry point into the script
def main(argv=None):
    # Print some info
    print
    print "This tool is a sample script that queries the ArcGIS Server logs and writes a report"
    print "  summarizing all map service draws within the past 24 hours."
    print
    
    # Ask for admin/publisher user name and password
    username = raw_input("Enter user name: ")
    password = getpass.getpass("Enter password: ")
 
    
    # Ask for server name
    serverName = raw_input("Enter Server name: ")
    serverPort = 6080

    # Ask for text file path
    filePath = raw_input("Enter the path of the text file where the statistics should be written.")

    millisecondsToQuery = 86400000 # One day 
    hitDict = {}
    
    # Get a token
    token = getToken(username, password, serverName, serverPort)
    if token == "":
        print "Could not generate a token with the username and password provided."
        return
    
    # Construct URL to query the logs
    logQueryURL = "/arcgis/admin/logs/query"
    startTime = int(round(time.time() * 1000))
    endTime = startTime - millisecondsToQuery
    logFilter = "{'services':'*','server':'*','machines':'*'}"
    
    params = urllib.urlencode({'level': 'FINE', 'startTime': startTime, 'endTime': endTime, 'filter':logFilter, 'token': token, 'f': 'json'})
    
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    
    # Connect to URL and post parameters    
    httpConn = httplib.HTTPConnection(serverName, serverPort)
    httpConn.request("POST", logQueryURL, params, headers)
    
    # Read response
    response = httpConn.getresponse()
    if (response.status != 200):
        httpConn.close()
        print "Error while querying logs."
        return
    else:
        data = response.read()

        # Check that data returned is not an error object
        if not assertJsonSuccess(data):          
            print "Error returned by operation. " + data
        else:
            print "Operation completed successfully!"

        # Deserialize response into Python object
        dataObj = json.loads(data)
        httpConn.close()

        # Need these variables to calculate average draw time for an ExportMapImage call
        mapDraws = 0
        totalDrawTime = 0 
        
        # Iterate over messages        
        for item in dataObj["logMessages"]:
            
                       
            if item["message"] == "End ExportMapImage":

                elapsed = float(item["elapsed"])
                keyCheck = item["source"]

                if keyCheck in hitDict:
                    stats = hitDict[keyCheck]

                    # Add 1 to tally of hits
                    stats[0] += 1
                    
                    # Add elapsed time to total elapsed time
                    stats[1] += elapsed
                else:
                    # Add key with one hit and total elapsed time
                    hitDict[keyCheck] = [1,elapsed]

        # Open text file and write header line       
        summaryFile = open(filePath, "w")        
        header = "Service,Number of hits,Average seconds per draw\n"
        summaryFile.write(header)

        # Read through dictionary and write totals into file 
        for key in hitDict:

            # Calculate average elapsed time
            totalDraws = hitDict[key][0]
            totalElapsed = hitDict[key][1]
            avgElapsed = 0

            if totalDraws > 0:     
                avgElapsed = (1.0 * (totalElapsed / totalDraws)) #Elapsed time divided by hits

            # Construct and write the comma-separated line         
            line = key + "," + str(totalDraws) + "," + str(avgElapsed) + "\n"
            summaryFile.write(line)

        summaryFile.close()
        return

#A function to generate a token given username, password and the adminURL.
def getToken(username, password, serverName, serverPort):
    # Token URL is typically http://server[:port]/arcgis/admin/generateToken
    tokenURL = "/arcgis/admin/generateToken"
    
    # URL-encode the token parameters
    params = urllib.urlencode({'username': username, 'password': password, 'client': 'requestip', 'f': 'json'})
    
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    
    # Connect to URL and post parameters
    httpConn = httplib.HTTPConnection(serverName, serverPort)
    httpConn.request("POST", tokenURL, params, headers)
    
    # Read response
    response = httpConn.getresponse()
    if (response.status != 200):
        httpConn.close()
        print "Error while fetching tokens from admin URL. Please check the URL and try again."
        return
    else:
        data = response.read()
        httpConn.close()
        
        # Check that data returned is not an error object
        if not assertJsonSuccess(data):            
            return
        
        # Extract the toke from it
        token = json.loads(data)       
        return token['token']            
        

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
    sys.exit(main(sys.argv[1:]))
