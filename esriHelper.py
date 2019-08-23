# esriHelper Class (designed for python 3.6.8) 
import arcpy
import datetime
import os

class esriHelper:

    def __init__(self, logname, loglocation):
        self.loglocation = loglocation
        self.logname = logname

    def writeToLog(self, message):
        # Purpose: to write a string to a text file; used as a program event log
        # Input:  Text String
        # Output: A text file with the input text string appended to it.
        
        # writes text to a text file.
        logName = self.loglocation + '//' + self.logname +'_' + datetime.date.today().strftime("%Y_%B_%d") + ".txt"
        log = open(logName, 'a')
        log.write('\n' + datetime.datetime.today().strftime('%m/%d/%Y - %H:%M:%S:%f') + ' - ' + message + '\n')
        log.close()

    def writeGPToLog(self):
        # Purpose: Dump the latest 3 lines of the esri GeoProcessing log to a text file written by the writeToLog() function.
        # Input: None 
        # Output: Write the last 3 lines of the current Geoprocessing log  to the text log file created by the writeToLog() function.
        self.writeToLog(arcpy.GetMessages())

    def returnFieldMap(self, fc):
        # Purpose: Create a field map for the inputted feature class for use with GP tools
        # Input: The path to the feature class as a sting value
        # Output: A fieldmappings object that has the proper field mappings for the inputted feature class
        self.writeToLog('Creating field map for feature class: ' + fc)
        fieldmappings = arcpy.FieldMappings()
        fieldmappings.addTable(fc)
        self.writeToLog ('Successfully added field map for FC')
        return fieldmappings

    def deleteFile(self, path, type):
        # Purpose: Use the ArcPy library to delete an object
        # Input: FQDN to source, Data type
        # Output: None (desired object is deleted from system)
        if arcpy.Exists(path):
            arcpy.Delete_management(path, type)
            self.writeGPToLog()
        else:
            self.writeToLog(path + "doesn't exist!") 

    def dataType(self, fc, quality):
        # Purpose: use the describe method to report information about an esri feature
        # Input: an esri feature class
        # Output: a String describing the feature type
        desc = arcpy.Describe(fc)
        # Check the feature class feature type
        if quality == 'featureType':
            return desc.featureType
        # Check if Feature class has spatial index
        elif quality == 'SI':
            return desc.hasSpatialIndex
        elif quality == 'shapeType':
            return desc.shapeType
        elif quality == 'Z':
            return desc.hasZ
        else:
            return None 

    def buildLayerSyntax(self, FC):
        # Purpose: build a field layer string for layer operations
        # Input: an esri feature class
        # Output: a String of fields useable by the esri gp engine for layer tools
        layerString = ''
        fieldList = arcpy.ListFields(FC)

        for field in fieldList:
            buildString = None
            buildString = field.name + " " + field.name + " VISIBLE NONE;"
            layerString += buildString

        return layerString

    def createDB(self, name, path):
        # Purpose: Creates a Current version empty File Geodatabase
        # Input: String representing the name of a File Geodatabase
        # Output: An empty esri current version File Geodatabase

        if (name[-4:].upper() == '.FGB'):
            name2 = name
            self.writeToLog ('db ' + name + ' name has .fgb extension')
        else:
            name2 = name + '.gdb'
            self.writeToLog ('db ' + name + ' name does not have .fgb extension - adding')
        
        try:
            self.log.writeToLog(path + '\\' + name2)
            if arcpy.Exists(path + '\\' + name2):
                self.writeToLog(name + '  already Exists!  Deleting current version...')
                self.deleteFile(path + '\\' + name2, 'Workspace')
            else:
                self.writeToLog('No database existing, creating database ' + name2)
                arcpy.CreateFileGDB_management(path, name2, "CURRENT")
                self.writeToLog('created fgb ' + name2 + '.gdb')
                self.writeGPToLog()
        except arcpy.ExecuteError:
                self.writeGPToLog()

    def returnPath(self, string, switch):
        # Purpose:  break a file path into either a path string or a file string
        # Input: String
        # Output: Sting of either the path or the file, depending on switch (boolean)
        position = string.rfind(os.sep)
        if switch:
            return string[position + 1:] 
        else:
            return string[:position]

