"""
IsAType is a collection of static methods that check for specific types of data contained
in our MSU schedule of classes. Of course these are not strictly accurate, since they only
check that a field fits a few specific patterns (e.g Five characters long and all integers
or two capital letters etc.)
"""

class IsAType:
    """Not really used to its fullest, but I thought that if I needed to verify each field in the input (at least a loose verification)
       that I would need tests for each type. 
    """
    @staticmethod
    def isInt(s):
        """Can this value be an integer?

        Args:
            s (string): Possible string to be an int

        Returns:
            bool: True if it can be an integer
        """
        try: 
            int(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def isACrn(crn):
        """Possible Course Registration Number that needs to be an integer of 5 digits in length.

        Args:
            crn (string): The possible course num

        Returns:
            bool: True = possible crn.
        """
        return len(crn) == 5 and IsAType.isInt(crn)

    @staticmethod
    def isADayTime(dt):
        """ Checks if an entry is a class time for a course in the schedule. Checks if the first
            four characters can be a number (like for a time) followed by two characters that contain
            am or pm.
        Params:
            dt (string) : Four digit time with an 'am' or 'pm' at the end.

        Returns:
            bool : True  = itt fits the daytime pattern like 1300pm or 0900am
        """
        return IsAType.isInt(dt[:4]) and dt[4:6] in ['am','pm']

    @staticmethod
    def isAClassDays(days):
        """Checks to see if string is a valid class days string. 

        Args:
            days (string): A string like MWF or TR depicting what days a class is on. If the string only consisting of the 
                        letters "MTWRFSU" and only one of each, then it is a Class Day identifier

        Returns:
            Bool :  True = the string is something like MWF or TR or F or MF any pattern with single 
                    instances of "MTWRFSU" these characters.
        """
        valid =  "MTWRFSU"

        checksum = 0
        dups = ""
        for d in days:

            # counting that all letters are valid
            if d in valid:
                checksum +=1 
            
            # checking for duplicate letters
            if not d in dups:
                dups += d
            else:
                return False
        
        return checksum == len(days)

    @staticmethod
    def isASectionNum(n,sem='FALL'):
        """Is this a possible section number 

            Fall start with 1 like 101
            Spring start with 2 like 201
            Summer1 start with 3 like 301
            Summer2 start with 4 like 401

        Args:
            n (string): Possible section number

        Returns:
            bool: True = 3 digit number beginning with proper digit for semester

        Todo:
            INCOMPLETE: Section numbers are all over the place and not jsut digits.
                        More checking needed. 
        """
        semester_vals = {'FALL':'1','SPRING':'2','SUMMER_1':'3','SUMMER_2':'4'}

        if len(n) == 3:
            if IsAType.isInt(n) and n[0] == semester_vals[sem]:
                return True
            if n[0] == 'X' and n[1] == semester_vals[sem]:
                return True
            if n[1:] in ['MX','DX']:
                return True
        
        return False

    @staticmethod
    def isABuildingAbbr(b):
        """Is this a building abbreviation

        Args:
            b (string): A possible building abbreviation

        Returns:
            bool: True = It is a two character uppercase string like :BO or DB
        """
        if len(b) == 2 and b.isupper():
            return True
        return False

    @staticmethod
    def isASubj(s):
        """Is this a subject abbreviation

        Args:
            b (string): A possible subject abbreviation

        Returns:
            bool: True = Four characters long and all letters and all uppercase.
        """
        if len(s) == 4 and s.isalpha() and s.isupper():
            return True
        return False

if __name__ == '__main__':
    pass

