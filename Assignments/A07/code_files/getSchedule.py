#!/usr/local/bin/python3

from datetime import datetime
import os
from collections import OrderedDict
import json
import PyPDF2
import re
import requests
from isAType import IsAType


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__today__ = datetime.today()
__year__ = __today__.year

__headers__ = ['Col', 'PT', 'Crn', 'Subj', 'Crse', 'Sect', 'Title', 'PrimaryInstructor', 'Max', 'Curr', 'Aval', 'Days', 'Begin', 'End', 'Bldg', 'Room']
__colleges__ = ['BA','FA','HH','ED','SE','BA','HM','UN']
__subjects__ = ['ACCT', 'AGBU', 'AMUS', 'ART', 'ATRN', 'BAAS', 'BIOL', 'BUAD', 'CHEM', 'CMPS', 'COUN', 'CRJU', 'DNHY', 'ECED', 'ECON', 'EDBE', 'EDLE', 'EDUC', 'ENGL', 'ENSC', 'EPSY', 'ETEC', 'EXPH', 'FINC', 'FREN', 'GEOG', 'GEOS', 'GERM', 'GLBS', 'GNMT', 'GNSC', 'HIST', 'HSAD', 'HSHS', 'HUMN', 'IDT', 'KNES', 'LSBA', 'MATH', 'MCOM', 'MENG', 'MGMT', 'MIS', 'MKTG', 'MLSC', 'MUSC', 'MWSU', 'NURS', 'PETE', 'PHIL', 'PHYS', 'POLS', 'PSYC', 'RADS', 'READ', 'RESP', 'SOCL', 'SOST', 'SOWK', 'SPAD', 'SPAN', 'SPCH', 'SPED', 'STAT', 'STEM', 'TECH', 'THEA', 'WGST']
__days__ = ['MW', 'TR', 'W', 'T', 'MWF', 'F', 'R', 'M', 'MS', 'MTWR', 'MTRF', 'MF', 'FM', 'MWSU', 'WF', 'MR', 'RF', 'SU', 'S', 'MTR']
__buildings__ = ['DB', 'FA', 'CO', 'BO', 'MY', 'BH', 'MA', 'CE', 'PY', 'BW', 'OR', 'VB', 'TC', 'HA', 'FM', 'LI', 'CL']
__sections__ = ['101', '102', '103', '170', '180', '104', '105', '106', '107', '108', 'ART', 'X10', 'X11', '190', '191', '192', '193', '194', '195', '196', 'DX1', 'X1A', '11A', '11B', '11C', '11D', '11E', '11F', '1H1', '1HA', '11G', '11H', '11I', 'X1B', 'L10', 'L11', '181', '1H2', 'X12', 'X13', 'X14', 'X15', 'X16', 'X17', 'X18', 'DX2', 'L12', 'DX3', '1R1', '1R2', '1R3', '1R4', '1R5', 'XR6', '1R6', 'L13', 'XR1', 'XR2', '109', '110', '111', '112', '113', '114', 'DXA', '201', 'IDT', 'L20', 'L21', 'L19', 'J01', 'JX1', 'MIS', 'L14', 'L15', 'L16', 'L17', 'L18', 'L22', 'DX4', 'V10']
__dayTimes__ = ['0200pm', '0320pm', '1230pm', '0150pm', '0930am', '1050am', '1100am', '1220pm', '0800am', '0920am', '0530pm', '0820pm', '0500pm', '0750pm', '0450pm', '0900am', '1150am', '0100pm', '1000am', '0850am', '0300pm', '0350pm', '0950am', '0130pm', '0400pm', '0550pm', '0250pm', '0650pm', '0330pm', '0520pm', '0220pm', '0420pm', '0430pm', '0720pm', '0620pm', '1200pm', '1250pm', '0305pm', '0310pm', '0510pm', '0515pm', '0715pm', '0920pm', '0600pm', '0850pm', '1120am', '0230pm', '0205pm', '1055am', '0740am', '0915am', '1020am', '0120pm', '0700pm', '0950pm', '0201pm', '0301pm', '0401pm', '1030am', '0830pm', '0730am', '0830am', '0630am', '0700am', '0730pm', '0630pm', '0750am', '0240pm', '1130am', '0940am']



class GetSchedule:
    def __init__(self,**kwargs):

        self.semester = kwargs.get('semester','FALL')
        self.redownload = kwargs.get('redownload',False)

        self.pdfFileName = None     # Name of and location of downloaded pdf schedule
        self.year = __year__        # Current year
              
        self.savePath = os.path.join(__location__,'schedules')
        self.pdfRef = None          # A pypdf type that holds the downloaded pdf schedule
        self.addHeaders = True     # Add column headers to json when saving or not
        self.pdfText = []           # List of processed text pulled from pdf doc

        self.headers = ['Col', 'Crn', 'Subj', 'Crse', 'Sect', 'Title', 'PrimaryInstructor', 'Max', 'Curr', 'Aval', 'Days', 'Begin', 'End', 'Bldg', 'Room']
        self.validSemesters = ['FALL','SPRING','SUMMER_1','SUMMER_2']


        self.keepers = ['Col', 'Crn', 'Subj', 'Crse', 'Sect', 'Title', 'PrimaryInstructor', 'Max', 'Curr', 'Aval', 'Days', 'Begin', 'End', 'Bldg', 'Room']

        if not os.path.isdir(self.savePath):
            os.mkdir(self.savePath,mode=755)

        if self.redownload:
            self.loadSchedule()
        else:
            self._loadSavedSchedule()

    def _getSchedule(self,semester='FALL'):
        """get the msu class schedule from the specified url

        Args:
            semester (str, optional): Semester identifier. Defaults to 'FALL'.
            savePath (str, optional): String path. Defaults to '.' (local directory).

        Raises:
            ValueError: Error for wrong semester identifier.

        Returns:
            bool: True = a file was downloaded and saved.
        """
        

        if not semester.upper() in self.validSemesters:
            raise ValueError(f'The semester value: `{semester}` is not valid! Needs to be in: {self.validSemesters}')

        url = f"https://secure.msutexas.edu/argos-reports/registrar/Schedule_For_Faculty_{semester}.pdf"

        self.pdfFileName = os.path.join(self.savePath,f'{__year__}_{semester.lower()}_schedule.pdf')

        response = requests.get(url)
        with open(self.pdfFileName,"wb") as f:
            f.write(response.content)

        if not os.path.isfile(self.pdfFileName):
            raise ValueError(f'The file at: `{self.pdfFileName}` did not get saved!')

        
    def _loadSavedPdf(self):
        """Loads the local MSU schedule downloaded from the internets.

        Args:
            path (str, optional): Path to the downloaded schedule. Defaults to None.

        Raises:
            ValueError: Error for wrong file path.

        Returns:

            list or None: list of each line in the schedule or none if empty.

        """

        if not os.path.isfile(self.pdfFileName):
            error = f'The path value: `{self.pdfFileName}` is not a valid file path!'
            raise ValueError(error)

        # creating a pdf file object
        pdfFileObj = open(self.pdfFileName, 'rb')

        # creating a pdf reader object
        self.pdfRef = PyPDF2.PdfFileReader(pdfFileObj)

    def _extractText(self):
        """Extract text from a schedule line and clean it in the process. 

        Args:
            pdf (pdf): rb version of a pdf file

        Returns:
            list: List of lists of each schedule lines components (hopefully)
        """
        self.pdfText = []

        # loop through a page at a time
        for i in range(self.pdfRef.numPages):
            pageObj = self.pdfRef.getPage(i)   # pdflib reference to a page
            text = pageObj.extractText()    # pdflib extract text (pseudo unformatted sadly) 

            text = text.replace(",","")
            # replace new lines with commas (separate fields ... kinda)
            text = text.replace("\n",",")

            # now make multi-space gaps newlines (separate lines)
            text = re.sub("\s{2,}", '\n', text)
            
            # Look for the PM in Last Run: 6/17/2021 5:56:12 PM
            # which has a comma after it now.
            pos = text.find("PM,") 
            if pos < 0:
                pos = text.find("AM,") 
            # If we found it, extract all those characters
            if pos:
                text = text[pos+3:]

            # now after replacing newlines with commas and then multi-space gaps with newlines
            # we split a chunk of text on the newlines as this actually represents a single line
            # in the pdf schedule
            lines = text.split("\n")

            # do some more cleaning (really insuring values are in right columns)
            lines = self._cleanLines(lines)
            self.pdfText.extend(lines)
        self._saveJsonFile()


    def _saveJsonFile(self):

        if not self.semester:
            raise ValueError("Error: cannot save Json file with 'semester' value being set!")

        self.jsonFileName = os.path.join(self.savePath,f'{self.year}_{self.semester.lower()}_schedule.json')

        if self.addHeaders:
            newDict = []
            for line in self.pdfText:
                newDict.append(self._zipJson(line))

        with open(self.jsonFileName,"w") as f:
            if self.addHeaders:
                jdata = json.dumps(newDict,indent=4)
            else:
                jdata = json.dumps(self.pdfText,indent=4)
            f.write(jdata)

    def _cleanLines(self,lines):
        """Takes a list of schedule entries and replaces some values or moves others to make
           sure that correct values are in the correct columns.

        Args:
            lines (list): List of text entries from schedule

        Returns:
            list :  Cleaned text lines. 
        """
        cleanLines = []
        
        for line in lines:
            # remove leading or trailing commas
            line = line.strip(",")
            # turn single line into cells by splitting on commas
            line = line.split(",")

            # If first entry isn't a two character college values, shift over by one.
            if not line[0] in __colleges__:
                line = line[1:]

            # Clean or Add more Processing Here...
            
            # If the "crn" value is not there, but in a place holder
            if len(line) > 0 and not IsAType.isACrn(line[1]):
                line.insert(1,'-----')

            # create empty list in case we have a long line with sub-lines
            newLines = None

            # If the line is bigger than any entry should be it contains multiple schedule entries
            # so we need to turn it into one big long string, then split on the value that each
            # entry should begin with (college abbreviation)
            if len(line) > 20:
                college = line[0]                   # find the college entry (first value of every line)
                newLine = ','.join(line)            # implode list using commas 
                newLines = newLine.split(college)   # now split on college abbreviation

            # if we had a big line, process the new sublines created and turn those into
            # single schedule (class) entries.
            if newLines:
                for sub in newLines:
                    sub = sub.strip(",")
                    sub = sub.split(",")
                    if len(sub) > 0:
                        cleanLines.append(sub)
            # other wise append the line to our cleanLines list
            else:
                if len(line) > 1:
                    cleanLines.append(line)
        
        for i in range(len(cleanLines)):
            if len(cleanLines[i]) > 9:
                if cleanLines[i][9] in __days__:
                    # a = cleanLines[i][:9]
                    # b = cleanLines[i][9:]
                    # c = [' ']
                    # a.extend(c).extend(b)
                    cleanLines[i] = cleanLines[i][:9] + [' '] + cleanLines[i][9:]
                    
        return cleanLines

    def _loadSavedSchedule(self,semester=None):
        if semester:
            self.semester = semester

        self.jsonFileName = os.path.join(self.savePath,f'{self.year}_{self.semester.lower()}_schedule.json')

        if not os.path.isfile(self.jsonFileName):
            error = f"Error: {self.jsonFileName} is NOT a file! Where did it go??"
            raise ValueError(error)
        
        with open(self.jsonFileName) as f:
            data = f.read()
            self.pdfText = json.loads(data)
        

    def _zipJson(self,line):
        """Turn line of values (cells) into a dictionary (or json if you wish).

        Args:
            line (list): All the values in a single schedule entry

        Returns:
            dict: Dictionary of cleaned schedule values in dictionary format. 
        """

        newdict = OrderedDict()
        i = 0
        for item in line:
            if i == len(self.headers):
                continue
            if self.headers[i] in self.keepers:
                newdict[self.headers[i]] = item
            i += 1

        return newdict

    def loadSchedule(self,semester=None,redownload=False):
        """Grab class schedule from MSU website if necessary, then save and process pdf to get text.

        Args: 
            semester (str): FALL,SPRING,SUMMER_1,SUMMER_2.
            redownload (bool,): True = go get new copy from web. Defaults to True.
        """
        if semester:
            self.semester = semester

        if redownload:
            print("setting redownload...")
            self.redownload = redownload

        self.pdfFileName = os.path.join(self.savePath,f'{self.year}_{self.semester.lower()}_schedule.pdf')

        if self.redownload:
            print("doing redownload...")
            self._getSchedule(self.semester)
            self._loadSavedPdf()
            self._extractText()
        else:
            self._loadSavedSchedule()

    def setKeepers(self,keepers):
        # set keepers to keep nothing
        self.keepers = []
        for col in keepers:
            if col in self.headers:
                self.keepers.append(col)
            else:
                error = f"Column: {col} is not a valid column name in the schedule table!"
                raise ValueError(error)



if __name__=='__main__':
    
    semesters = ['FALL','SPRING','SUMMER_1','SUMMER_2']
    # getSchedule('FALL')
    # pdf = loadLocalSchedule("2021_FALL_schedule.pdf")

    # getSchedule('SPRING')
    # pdf = loadLocalSchedule("2021_spring_schedule.pdf")

    #getSchedule('SUMMER_1')
    #pdf = loadLocalSchedule("2021_summer_1_schedule.pdf")

    rs = GetSchedule(redownload=True)
    
    #['Col', 'Crn', 'Subj', 'Crse', 'Sect', 'Title', 'PrimaryInstructor', 'Max', 'Curr', 'Aval', 'Days', 'Begin', 'End', 'Bldg', 'Room']
    #rs.setKeepers(['Crn', 'Subj', 'Crse', 'Sect', 'Title','Days', 'Begin', 'End', 'Bldg', 'Room'])
    for semester in semesters:
        rs.loadSchedule(semester,True)
    

