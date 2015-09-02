<?php

if (!debug_backtrace()) {
    $dbinfo = json_decode(file_get_contents("config.mysqli.json"));
    print_r($dbinfo);
    $myDB = new myMysqli($dbinfo->user,$dbinfo->password,$dbinfo->host,$dbinfo->dbname);
}

/**
* myMysqli - wrapper class that offers little improved usage of the mysqli PDO
* class.  It does group commonly used functions together providing
* a self documented "quick reference" to quickly execute queries and obtain
* their results.
*/
class myMysqli{
    var $Username;          //username for mysql connection
    var $Pasword;           //password for mysql connection
    var $Host;              //Host name
    var $DbName;             //Database Name
    var $Conn;              //Datavase connection var
    var $Error;             //Error var
    var $Result;            //Var to hold query results

    function __construct($user_name,$password,$host,$db_name){
        $this->Username = $user_name;
        $this->Password = $password;
        $this->Host = $host;
        $this->DbName = $db_name;
        $this->Conn = new mysqli($this->Host, $this->Username, $this->Password ,$this->DbName);
        if($this->Conn->connect_errno > 0){
            $this->Error = $this->Conn->connect_error;
            return false;
        }
        $this->Error = null;
        return true;
    }

    /**
    * AffectedRows - Returns number of rows that were affected in db
    *
    * @params - void
    * @returns - int
    */
    function AffectedRows(){
        return $this->Result->affected_rows;
    }

    /**
    * NumRows - Returns number of rows in result
    *
    * @params - void
    * @returns - int
    */
    function NumRows(){
        return $this->Result->num_rows;
    }

    /**
    * GetError - If RunSql or the constructor return false, the error
    *            will be in $this->Error
    *
    * @params -
    * @returns -
    */
    function GetError(){
        return $this->Error;
    }

    /**
    * GetResult - Returns a SINGLE row from the result set. Can be used
    * to traverse the query set, but it's inteded for single row results.
    *
    * @params - void
    * @returns - mixed - bool = false on failure, or associated array on success
    */
    function GetResult(){
        if( $result = $this->Result->fetch_assoc()){
            return $result;
        }
        return false;
    }

    /**
    * GetResults - Returns ALL rows from the result set in an array.
    *
    * @params - void
    * @returns - mixed - bool = false on failure, or associated array on success
    */
    function GetResults(){
        $rows = array();
        while($row = $this->Result->fetch_assoc()){
            $rows[] = $row;
        }
        return $rows;
    }

    /**
    * RunSql - Actually executes a sql statement.
    *
    * @params - string - query string
    * @returns - bool
    */
    function RunSql($sql){
        if(!$this->Result = $this->Conn->query($sql)){
            $this->Error = $this->Conn->error;
            return false;
        }
        return true;
    }

}
