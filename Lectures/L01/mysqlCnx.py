import mysql.connector  #apt install python3-mysql.connector
import os,sys
import json             # 

# https://www.w3schools.com/python/python_mysql_getstarted.asp

class MysqlCnx:
    """A mysql.connector facade class to "ease" the use of connecting to and working with a 
    mysql database.  

    References:
        - mysql.connector
        - json

    """
    def __init__(self, **kwargs):
        """
        Keyword Args:
            host (string)       :  db host to connect to.
            user (string)       :  Username to auth with.
            passwd (string)     :  Password of db user.
            database (string)   :  Name of database.
            auth_plugin (string):  Type of authentication for mysql (e.g. 'mysql_native_password')
        """

        self.host = kwargs.get('host', 'localhost')
        self.user = kwargs.get('user', None)
        self.passwd = kwargs.get('passwd', None)
        self.database = None
        if 'db' in kwargs:
            self.database = kwargs['db']
        elif 'database' in kwargs:
            self.database = kwargs['database']
        self.auth_plugin = kwargs.get('auth_plugin', 'mysql_native_password')

        
        # print(f"{self.host} {self.passwd} {self.user} {self.database} {self.auth_plugin} ")


        """Return a python dictionary as a result instead of a list"""
        self.returnDict = True

        self.cnx = mysql.connector.connect(host=self.host,
                                           user=self.user,
                                           password=self.passwd,
                                           database=self.database,
                                           auth_plugin=self.auth_plugin)


     
    def _response(self, **kwargs):
        """ Format a consistent response for all public functions. It's a little silly 
            right now, as it just returns what gets passed in. But it may have more use in 
            the future with added logic.

        Args:
            kwargs (dict) : everything you want sent back in the response to the client

        Returns:
            dict : dictionary that includes the following:
                    data (list)     : list of resulting rows
                    success (bool)  : True = successful
                    message (string): A message of action that happened
                    error (string)  : error if any
        """
        r = {}
        r['data'] = kwargs.get('data', None)
        r['success'] = kwargs.get('success', False)
        r['message'] = kwargs.get('message', None)
        r['error'] = kwargs.get('error', None)
        return r



    def _runQuery(self, sql, dct=False):
        """Method to run a query and capture an error before it crashes  our little api. 

        Args:
            sql (string) : sql statement to be run
            dct (bool) : True = results come back in dictionary form

        Returns:
            json : response that contains success or error messages along with the 
                            result cursor provided by our DB
        """
        response = {'success': True}  #
        try:
            # try and run the query
            cursor = self.cnx.cursor(dictionary=dct)
            cursor.execute(sql)
            # successful query, place result in response dictionary
            response['cursor'] = cursor
        except mysql.connector.Error as err:
            response['success'] = False
            response['error'] = err

        return response

    def queryOne(self, sql, dct=True):
        """Method to run a query and get single row result.

        Args:
            sql (string) : sql statement to be run
            dct (bool) : True = results come back in dictionary form

        Returns:
            json : response that contains success or error messages along with the 
                            result cursor provided by our DB
        """
        res = self.query(sql, dct)

        if len(res['data']) > 0:
            res['data'] = res['data'][0]

        return res

    def query(self, sql, dct=True):
        """Runs a sql query invoking some private methods to return a consistent response as well as catch errors.

        Args:
            sql (string) : sql statement to be run
            dct (bool) : True = results come back in dictionary form

        Returns:
            json : response that contains success or error messages along with the 
                            result cursor provided by our DB
        """
        data = []
        queryTypes = ['select', 'insert', 'update', 'delete', 'create', 'drop']
        queryVerbs = [
            'selected', 'inserted', 'updated', 'deleted', 'created', 'dropped'
        ]
        queryType = None
        error = None  # error message if any
        success = False  # hoping for success
        message = None  # clarification of events

        # look for key word to determine how to handle the query
        for qtype in queryTypes:
            if qtype in sql.lower():
                queryType = qtype
                i = queryTypes.index(queryType)
                queryVerb = queryVerbs[i]

        tableName = self._getTableName(sql)  # get table name from sql

        if 'select' in sql.lower():
            result = self._runQuery(sql, dct)  # run query
        else:
            result = self._runQuery(sql)

        success = result['success']

        if success:
            if not queryType in ['select']:
                self.cnx.commit()
                effectedRows = result['cursor'].rowcount
            else:
                rows = result['cursor'].fetchall()  # get data from result dictionary
                for row in rows:  # build list to return
                    data.append(row)
                effectedRows = len(data)
                #message = f"{queryVerb.capitalize()} {effectedRows} rows from {tableName}"

            if queryType in ['insert', 'update', 'delete', 'select']:

                message = f"{queryVerb.capitalize()} {effectedRows} rows. Table = {tableName}"

            if queryType in ['drop', 'create']:
                message = f"{queryVerb.capitalize()} table {tableName}"

        else:
            error = result['error']

        return self._response(success=success,
                              message=message,
                              error=error,
                              data=data)
    def _getTableName(self, sql):
        """ Pulls the table name out of sql statements (so we can use it to
            test if rows got inserted for example).

        Args:
            sql (string)   : sql statement to analyzed

        Returns:
            string       : table name pulled out of sql statement
            
        """
        keywords = ['into', 'update', 'from', 'create', 'drop']
        sql = sql.replace("`", "")
        sql = sql.replace("'", "")
        parts = sql.split()
        #print(parts)
        for part in parts:
            if part.lower() in keywords:
                j = 1
                if part.lower() in ['create', 'drop']:
                    j = 2

                i = parts.index(part)
                if len(parts) > i + j:
                    return parts[i + j]
        return None


if __name__ == '__main__':

    with open('.config.json') as f:
        config = json.loads(f.read())

    cnx = MysqlCnx(**config)

    # result = cnx.query("SELECT * FROM `nfl_week_max`")

    # if result['success']:
    #     for row in result['data']:
    #         print(row)


    sql = "DROP TABLE tuts2"
    result = cnx.query(sql)
    print(result)


    sql = """
    CREATE TABLE tuts2 (
    id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL, 
    author VARCHAR(40) NOT NULL, 
    submission_date DATE, 
    PRIMARY KEY ( id )) 
    """

    result = cnx.query(sql)

    print(result)

    sql = "INSERT INTO tuts2 (`title`, `author`, `submission_date`) "
    sql += "VALUES('Learn PHP', 'Paul Hader Prescott', NOW())"
    result = cnx.query(sql)
    print(result)

    sql = "INSERT INTO tuts2 (`title`, `author`, `submission_date`) "
    sql += "VALUES('Learn MySQL', 'Ramesh Tableu', NOW())"
    result = cnx.query(sql)
    print(result)
    
    sql = "INSERT INTO tuts2 (`title`, `author`, `submission_date`) "
    sql += "VALUES('Learn Python', 'Bell Constrictor', NOW())"
    result = cnx.query(sql)
    print(result)
 