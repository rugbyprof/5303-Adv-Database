<?php

class myMysqli{
    var $Username;          //username for mysql connection
    var $Pasword;           //password for mysql connection
    var $Host;              //Host name
    var $DbName             //Database Name
    var $Conn;              //Datavase connection var
    var $Error;             //Error var
    var $Result;            //Var to hold query results

    function __construct($user_name,$password,$host,$db_name){
        $this->Username = $user_name;
        $this->$Password = $password;
        $this->$Host = $host;
        $this->DbName = $db_name;
        $this->Conn = new mysqli($this->Host, $this->Username, $this->$Password ,$this->DbName);
        if($this->Conn->connect_errno > 0){
            die('Unable to connect to database [' . $this->Conn->connect_error . ']');
        }
        $this->Error = null;
    }

    /**
    * AffectedRows - Returns number of rows that were affected in db
    *
    * @params - none
    * @returns - int - affected rows
    */
    function AffectedRows(){
        return $this->Result->affected_rows;
    }

    /**
    *
    *
    * @params -
    * @returns -
    */
    function NumRows(){
        return $this->Result->num_rows;
    }

    /**
    *
    *
    * @params -
    * @returns -
    */
    function GetError(){
        return $this->Error;
    }

    /**
    *
    *
    * @params -
    * @returns -
    */
    function GetResult(){
        return $this->Result->fetch_assoc();
    }

    /**
    *
    *
    * @params -
    * @returns -
    */
    function GetResults(){
        $rows = array();
        while($row = $this->Result->fetch_assoc()){
            $rows[] = $row;
        }
        return $rows;
    }

    /**
    *
    *
    * @params -
    * @returns -
    */
    function RunSql($sql){
        if(!$this->Result = $this->Conn->query($sql)){
            $this->Error = $this->Conn->error;
            return false;
        }
        return true;
    }

}
