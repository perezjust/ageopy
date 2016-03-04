# Name: sort_fields_v93.py
#
# Description
# -----------
# This script will permanently sort the records in a feature class
# and write the output to a new feature class or table. 
#
# Written By: Chris Snyder, WA DNR, 03/09/2008, chris.snyder(at)wadnr.gov
#
# Written For: Python 2.5.1 and ArcGIS v9.3.1 SP0
#
# UPDATES:
#
# Notes on input parameters (for the toolbox):
# VARIABLE             PAREMETER_INDEX     PARAMETER_DATA_TYPE
# -------------------------------------------------------------------
# inputFC              0                   TableView (the input FeatureClass, Table, FeatureLayer or TableView)
# outputFC             1                   DataSet (the output FeatureClass or Table)
# sortFieldName1       2                   Field
# sortFieldName1Method 3                   String ("ASCENDING","DESCENDING")
# sortFieldName2       4                   Field
# sortFieldName2Method 5                   String ("ASCENDING","DESCENDING")
# sortFieldName3       6                   Field
# sortFieldName3Method 7                   String ("ASCENDING","DESCENDING")

try:
    #Process: Import some modules
    import os, string, sys, time, traceback, arcgisscripting

    #Process: Create the gp object
    gp = arcgisscripting.create(9.3)

    #Process: Defines some functions used for getting messages from the gp and python
    def showGpMessage():
        gp.AddMessage(gp.GetMessages())
        print >> open(logFile, 'a'), gp.GetMessages()
        print gp.GetMessages()
    def showGpWarning():
        gp.AddWarning(gp.GetMessages())
        print >> open(logFile, 'a'), gp.GetMessages()
        print gp.GetMessages()
    def showGpError():
        gp.AddError(gp.GetMessages())
        print >> open(logFile, 'a'), gp.GetMessages()
        print gp.GetMessages()
    def showPyLog(): #just print to the log file!
        print >> open(logFile, 'a'), str(time.ctime()) + " - " + message
    def showPyMessage():
        gp.AddMessage(str(time.ctime()) + " - " + message)
        print >> open(logFile, 'a'), str(time.ctime()) + " - " + message
        print str(time.ctime()) + " - " + message
    def showPyWarning():
        gp.AddWarning(str(time.ctime()) + " - " + message)
        print >> open(logFile, 'a'), str(time.ctime()) + " - " + message
        print str(time.ctime()) + " - " + message
    def showPyError():
        gp.AddError(str(time.ctime()) + " - " + message)
        print >> open(logFile, 'a'), str(time.ctime()) + " - " + message
        print str(time.ctime()) + " - " + message

    #Specifies the root directory variable, defines the logFile variable, and does some minor error checking...
    dateTimeString = str(time.strftime('%Y%m%d%H%M%S'))
    scriptName = os.path.split(sys.argv[0])[-1].split(".")[0]
    userName = string.lower(os.environ.get("USERNAME")).replace(" ","_").replace(".","_")
    tempPathDir = os.environ["TEMP"]
    logFileDirectory = r"\\snarf\am\div_lm\ds\gis\tools\log_files"
    if os.path.exists(logFileDirectory) == True:
        logFile = os.path.join(logFileDirectory, scriptName + "_" + userName + "_" + dateTimeString + ".txt")
        try:
            print >> open(logFile, 'a'), "Write test successfull!"
        except:
            logFile = os.path.join(tempPathDir, scriptName + "_" + userName + "_" + dateTimeString + ".txt")  
    else:
        logFile = os.path.join(tempPathDir, scriptName + "_" + userName + "_" + dateTimeString + ".txt")
    if os.path.exists(logFile)== True:
        os.remove(logFile)
        message = "Created log file " + logFile; showPyMessage()
    message = "Running " + sys.argv[0]; showPyMessage()
    
    #Process: Check out the highest license available
    try:
        if gp.CheckProduct("ArcView") == "Available":
            gp.SetProduct("ArcView")
        elif gp.CheckProduct("ArcEditor") == "Available":
            gp.SetProduct("ArcEditor")
        elif gp.CheckProduct("ArcInfo") == "Available":
            gp.SetProduct("ArcInfo")
    except:
        message = "ERROR: Could not select an ArcGIS license level! Exiting script..."; showPyError(); sys.exit()
    message =  "Selected an " + gp.ProductInfo() + " license"; showPyMessage()

    #Process: Sets some gp environment variables
    gp.overwriteoutput = True

    #Process: Collect the input parameters
    inputLayer = gp.GetParameterAsText(0) #layer
    outputLayer = gp.GetParameterAsText(1) #featureclass
    sortFieldName1 = gp.GetParameterAsText(2)
    sortFieldName1Method = gp.GetParameterAsText(3)
    sortFieldName2 = gp.GetParameterAsText(4)
    sortFieldName2Method = gp.GetParameterAsText(5)
    sortFieldName3 = gp.GetParameterAsText(6)
    sortFieldName3Method = gp.GetParameterAsText(7)

    #Process: Print out the input parameters
    message = "INPUT PARAMETERS"; showPyMessage()
    message = "----------------"; showPyMessage()
    message = "Input Layer              = " + inputLayer; showPyMessage()
    message = "Output Layer             = " + outputLayer; showPyMessage()
    message = "Sort Field #1            = " + sortFieldName1; showPyMessage()
    message = "Sort Field #1 Method     = " + sortFieldName1Method; showPyMessage()
    message = "Sort Field #2            = " + sortFieldName2; showPyMessage()
    message = "Sort Field #2 Method     = " + sortFieldName2Method; showPyMessage()
    message = "Sort Field #3            = " + sortFieldName3; showPyMessage()
    message = "Sort Field #3 Method     = " + sortFieldName3Method + "\n"; showPyMessage()

    message = "Running error checks..."; showPyMessage()
    #Some error checking:
    try:
        dsc = gp.describe(inputLayer)
    except:
        message = "ERROR: Could not describe input layer! Exiting script..."; showPyError(); sys.exit()
    #make sure the inputLayer is a FeatureClass or Table
    inputLayerDataType = dsc.datasettype
    if inputLayerDataType not in ("FeatureClass","Table"):
        message = "ERROR: Input layer type (" + str(inputLayerDataType) + ") is not a FeatureClass or Table! Exiting script.."; showPyError(); sys.exit()
    #make sure the same field isn't trying to be sorted twice
    if (sortFieldName1 == sortFieldName2) or (sortFieldName2 not in ["","#"," "] and (sortFieldName2 == sortFieldName3)):
        message = "ERROR: Can't sort the same field twice! Exiting script..."; showPyError(); sys.exit()
    #Make sure a valid sort method is being provided
    fieldSortString = ""
    if sortFieldName1 not in ["","#"," "]:
        if sortFieldName1Method not in ["ASCENDING","DESCENDING"]:
            message = "ERROR: An invalid sort order was provided for sort field #1! Exiting script..."; showPyError(); sys.exit()
        else:
            fieldSortString = fieldSortString + sortFieldName1 + " " + sortFieldName1Method[0] + ";"
    if sortFieldName2 not in ["","#"," "]:
        if sortFieldName2Method not in ["ASCENDING","DESCENDING"]:
            message = "ERROR: An invalid sort order was provided for sort field #2! Exiting script..."; showPyError(); sys.exit()
        else:
            fieldSortString = fieldSortString + sortFieldName2 + " " + sortFieldName2Method[0] + ";"
    if sortFieldName3 not in ["","#"," "]:
        if sortFieldName3Method not in ["ASCENDING","DESCENDING"]:
            message = "ERROR: An invalid sort order was provided for sort field #3! Exiting script..."; showPyError(); sys.exit()
        else:
            fieldSortString = fieldSortString + sortFieldName3 + " " + sortFieldName3Method[0] + ";"
    outShpDbfFlag = False
    if inputLayer.split(".")[-1] not in ("shp","dbf") and outputLayer.split(".")[-1] in ("shp","dbf"):
        message = "WARNING: Some fields > 10 charaters in length may not be populated correctly - check the output!"; showPyWarning()
        outShpDbfFlag = True #field names in the output are limited to 10 charaters (used in the insertcursor)!
    message = "Error checks complete!"; showPyMessage()
    
    #Process: Create a blank feature class based on the schema of the input FC
    if inputLayerDataType == "FeatureClass":
        try:
            message = "Creating new output feature class..."; showPyMessage()
            shapeType = string.capitalize(dsc.shapetype)
            gp.CreateFeatureClass_management(str(os.path.split(outputLayer)[0]), str(os.path.split(outputLayer)[-1]), shapeType, dsc.catalogpath, "", "", dsc.spatialreference) 
        except:
            message = "ERROR: Could not create output feature class! Exiting script..."; showPyMessage()
    if inputLayerDataType == "Table":
        try:
            message = "Creating new output table..."; showPyMessage()
            gp.CreateTable_management(str(os.path.split(outputLayer)[0]), str(os.path.split(outputLayer)[-1]), dsc.catalogpath, "")
        except:
            message = "ERROR: Could not create output table! Exiting script..."; showPyMessage()
    
    #Process: Make a list of the field names in the input layer
    inputLayerFieldList = []
    for field in dsc.fields:
        inputLayerFieldList.append(field.name)

    #Process: Now write the sorted records to the new FC
    message = "Sorting fields..."; showPyMessage()
    searchRows = gp.searchcursor(inputLayer, "", "", "", fieldSortString[:-1])
    searchRow = searchRows.next()
    message = "Writing sorted records..."; showPyMessage()
    insertRows = gp.insertcursor(outputLayer)
    recordCount = 0
    while searchRow:
        insertRow = insertRows.newrow()
        for fieldName in inputLayerFieldList:
            try: #you can't write the OID, length, area, etc. fields!
                if outShpDbfFlag == False:
                    insertRow.setvalue(fieldName, searchRow.getvalue(fieldName))
                if outShpDbfFlag == True:
                    insertRow.setvalue(fieldName[0:10], searchRow.getvalue(fieldName))
            except:
                pass
        recordCount = recordCount + 1
        insertRows.insertrow(insertRow)        
        searchRow = searchRows.next()

    message = "Successfully wrote " + str(recordCount) + " records!"; showPyMessage()     

    #Process: Clean up the cursor objects
    del searchRow
    del searchRows
    del insertRow
    del insertRows
    
    message = scriptName + " is all done!"; showPyMessage()  
    
except:
    message = "\n*** PYTHON ERRORS *** "; showPyMessage()
    message = "Python Traceback Info: " + traceback.format_tb(sys.exc_info()[2])[0]; showPyMessage()
    message = "Python Error Info: " +  str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"; showPyMessage()
    message = "\n*** PYTHON LOCAL VARIABLE LIST ***"; showPyLog()
    variableCounter = 0                      
    while variableCounter < len(locals()):
        message =  str(list(locals())[variableCounter]) + " = " + str(locals()[list(locals())[variableCounter]]); showPyLog()
        variableCounter = variableCounter + 1