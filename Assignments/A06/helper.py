from typing import *    # used for `isinstance` comparing variable to q type
import pymongo          # used to connect to monDb
import glob             # used to read from directory using wildcard file matches
import json             # convert to and from json
import csv              # process csv files easily
import sys              # throw error messages and more
import os               # check file paths and more
from bson import json_util, ObjectId  # used to turn string id to Mongo _id


class PyMongoHelper:
    """ What it says: python mongodb helper
        https://pymongo.readthedocs.io/en/stable/tutorial.html
        https://pymongo.readthedocs.io/en/stable/api/index.html
    """
    def __init__(self,**kwargs):
        """Params:
                dbName          (string) - database name in mongo
                collectionName  (string) - :) you know
           Usage:
                dbcnx = PyMongoHelper(dbName='tempDB',collectionName='collectionTest')
                dbcnx.insert({some json object})
        """
        self.dbName = kwargs.get('dbName',None)
        self.collectionName = kwargs.get('collectionName',None)

        if not self.dbName:
            print(f"Error:  Needs a DB name passed in!")
            sys.exit(0)

        self.cnx = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.cnx[self.dbName]

        # if collectionName passed in, set it
        if self.collectionName:
            self.collection = self.db[self.collectionName]

    def setDb(self,name):
        """Set database name

        Args:
            name (string): string name of database
        """
        self.db = self.cnx[name]
    
    def setCollection(self,name):
        """Set collection name

        Args:
            name (string): name of collection
        """
        self.collectionName = name
        self.collection = self.db[self.collectionName]

    def emptyCurrentCollection(self):
        """Delete all documents from current collection
        """
        if self.collectionName:
            self.db[self.collectionName].delete_many({})
        #self.collection = self.db[self.collectionName]

    def getCollections(self):
        """Returns a list of collection names from the current db

        Returns:
            (list): of collection names
        """
        self.collections = self.db.list_collection_names()
        return self.collections

    def insert(self,document):
        """Insert object into db

        Args:
            document (json / dict): [description]

        Returns:
            (dict): dictionary of results with success or errors
        """
        if self.dbName == None:
            print("No DB name set in PyMongoHelper!")
            sys.exit()
        if self.collectionName == None:
            print("No collection name set in PyMongoHelper!")
            sys.exit()

        if not isinstance(document,List):
            return self.collection.insert_one(document)
        else:
            return self.collection.insert_many(document)


class FileProcessor:
    def __init__(self,**kwargs):
        """
        path = path to directory of files to process
        loadMongo = true or false
        """
        # Need a path to read files from
        self.filePath = kwargs.get('filePath',None)

        # if this is True, we will create json files with the 
        # same name as the csv/tsv files to save to
        self.saveToFile = kwargs.get('saveToFile',False)

        # A new folder name to save files to if you want otherwise
        # they get saved to same folder as csv/tsv files.
        self.savePath = kwargs.get('savePath',self.filePath)

        # if you want to load mongo set it to True and 
        # also pass in a DB name
        self.loadMongo = kwargs.get('loadMongo',False)
        self.dbName = kwargs.get('dbName',None)

        # which files do you want glob to match?
        self.globExt = kwargs.get('globExt','csv')

        # process the files automatically? 
        self.processFiles = kwargs.get('processFiles',False)

        # ERROR CHECKS!!
        # If you want to save to a folder and that save path doesn't exist ... error
        if self.savePath != None and not os.path.isdir(self.savePath):
            print(f"savePath: {self.savePath} is NOT a valid path!")
            sys.exit() 

        # folder name with csv/tsv files needs to exist
        if not os.path.isdir(self.filePath):
            print(f"Error: {self.filePath} is not a directory")
            sys.exit(0)

        # no DB name but you want to load mongo ... error
        if self.loadMongo:
            if self.dbName != None:
                self.dbcnx = PyMongoHelper(dbName=self.dbName)
            else:
                print("You cannot load mongo without a dbName!")
                sys.exit()

        if self.processFiles:
            self.readDir()  # read filenames from directory
            self._processFiles()

    def _processFiles(self):
        """ Private(ish) method to process a list of files stored in self.files
        """
        for fullName in self.files:
            print(f"Processing: {fullName}")
            self.csvToJson(csvFile=fullName,delimiter='\t',cleanCollection=True,chunkSize={'percent':1})


    def readDir(self,**kwargs):
        """ Reads a directory for files matching specific glob wildcard

        Returns:
            (list): List of files globbed from a directory
        """
    
        # use values passed in OR use the ones already set in the class
        filePath = kwargs.get('filePath',self.filePath)
        ext = kwargs.get('ext',self.globExt)

        # glob matches files, in this case "*.tsv"
        self.files = glob.glob(os.path.join(filePath ,f'*.{ext}'))

        return self.files

    def csvToJson(self,**kwargs):
        """ Csv or Tsv whatever. Just convert it to json and either save it to a file,
            load it into mongo, or return an array of values (don't to the last one for
            huge files)
            
            Returns:
                list of json objects if `returnList` keyword argument is True
        """
        csvFile = kwargs.get('csvFile',None)                 # Name of csv file with path to open  
        delimiter = kwargs.get('delimiter',',')              # tabs,commas,spaces,etc.
        colHeaders = kwargs.get('colHeaders',True)           # Are there column Headers?
        newLine = kwargs.get('newLine','\n')                 # The newline character (could be \r\n)
        returnList = kwargs.get('returnList',False)          # Return a list from this function?
        cleanCollection = kwargs.get('cleanCollection',False)# delete documents from collection
        chunkSize = kwargs.get('chunkSize',None)             # load data in chunks vs one at a time

        jsonDataArray = []                                   # list to hold json objects if needed

        name = os.path.basename(csvFile)                     # file base name no path 

        name, ext = os.path.splitext(name)                   # file name no extension

        if self.saveToFile:                                  # you know
            jsonName = os.path.join(self.savePath,name+".json")
            fp = open(jsonName,"w")
            print(f"Opening {jsonName} to write to...")
        
        if self.loadMongo:                                   # you know
            self.collectionName = name.replace('.','_')
            self.dbcnx.setCollection(self.collectionName)
            if cleanCollection:
                self.dbcnx.emptyCurrentCollection()
            print(f"Inserting {name} into {self.dbName}.{self.collectionName}")

        print(f"Getting filesize of {csvFile} ...")          # get lines in file to calculate % done
        numLines = sum(1 for line in open(csvFile))

        # I'm forcing chunksize to be 1% of fileSize
        chunkSize = int(numLines / 100)
        print(f"{csvFile} is {numLines} long and chunkSize = {chunkSize}...")

        # Used to print progress
        oldPercent = 0

        print("Processing file ...")
        with open(csvFile, newline=newLine,encoding='utf-8') as datafile:
            fileData = csv.reader(datafile, delimiter=delimiter)

            if colHeaders:
                self.colHeaders = next(fileData, None)
                next(fileData) # skip past column headers

            # init counter
            rowCount = 0

            # Length of the column headers (number of columns)
            headLen = len(self.colHeaders)

            # chunks are to load data as chunks instead of 
            # one obj at a time. So if a chunkSize is passed
            # in, we will insert a list of that size when it
            # fill up.
            if chunkSize:
                chunkList = []

            for row in fileData:
                # just in case col headers are not same length as data in row
                if(headLen == len(row)):
                    rowCount+=1

                    newPercent = round((rowCount/numLines)*100)
                    if newPercent != oldPercent:
                        print(f"{newPercent}% complete ...")
                        oldPercent = newPercent

                    # The json object with the keys and values that will get 
                    # loaded into mongo, or saved to a file, or returned from
                    # function call
                    jobj = {self.colHeaders[i]: row[i] for i in range(headLen)}

                    if self.loadMongo:
                        if chunkSize:
                            chunkList.append(jobj)
                        else:
                            res = self.dbcnx.insert(jobj)
                        if len(chunkList) == chunkSize:
                            #print("Inserting chunk ...")
                            res = self.dbcnx.insert(chunkList)
                            chunkList = []

                    if self.saveToFile:
                        # use json_util dumps instead of json.dumps because of ObjectId
                        fp.write(json_util.dumps(jobj))

                    if returnList:
                        jsonDataArray.append(jobj)

        if returnList:
            return jsonDataArray
            
        

if __name__=='__main__':
    from random import randint

    dbcnx = PyMongoHelper(dbName='tempDB',collectionName='collectionTest')

    # PymongoHelper insert one example
    # 10 individual object
    for i in range(10):
        res = dbcnx.insert({"testKey":randint(0,10000)})
        ack = res.acknowledged 
        id = res.inserted_id
        print(f"{ack}  -  {id}")

    # PymongoHelper insert many example
    # 1 list of 10 objects inserted as 10 single objects
    temp = []
    for i in range(10):
        temp.append({"anotherKey":randint(0,10000)})

    # insert list of objects
    res = dbcnx.insert(temp)

    ###################################################################

    # Example FileProcessor instance that will process the folder 
    # with all of the tsv files from Imdb.
    fp  = FileProcessor(
        filePath='./datasets.imdbws.com',
        saveToFile=True,
        savePath='./datasets.imdbws.com',
        loadMongo=True,
        dbName="moviesDb",
        globExt='tsv',
        processFiles=True)
                
                    


