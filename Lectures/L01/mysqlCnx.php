<?php

class MysqlCnx {

    public function __construct($host, $user, $passwd, $database) {
        // The Host, username, password, database from the config file.
        // This password should not end up in github.

        $this->conn = mysqli_connect($host, $user, $passwd, $database);

        if (mysqli_connect_errno()) {
            echo "Failed to connect to MySQL: " . mysqli_connect_error();
        }

        $this->response = [];
    }


    /**
     * query
     *
     * @description: returns a multi row result from db
     *
     * @param string $sql
     * @param bool $assoc - True = return associated array (key value) False = just array of values.
     * @return multi
     */
    public function query($sql, $assoc = true) {

        $this->response = [];

        $result = $this->runQuery($sql, $assoc);     // run the query 

        if ($result) {
            $this->response['success'] = true;

            $this->response['affectedRows'] = $this->affectedRows;

            // For single row results, just send back the result not
            // in an array (done for backwards compatibility)
            if (sizeof($this->resultData) == 1) {
                $this->response['data'] = array_pop($this->resultData);
            } else {
                $this->response['data'] = $this->resultData;
            }

        } else {
            $this->response['success'] = false;
            $this->response['error'] = $this->conn->error;
        }

        return $this->response;
    }

    /**
     * getQueryType
     * 
     * Determines the type of query being run ["SELECT",'insert','update','delete']
     *
     * @param string $sql Query being executed
     *
     * @return string
     */
    protected function getQueryType($sql) {
        if (strstr(strtoupper($sql), "SELECT") !== false) {
            return "SELECT";
        } else if (strstr(strtoupper($sql), "INSERT") !== false) {
            return "INSERT";
        } else if (strstr(strtoupper($sql), "UPDATE") !== false) {
            return "UPDATE";
        } else if (strstr(strtoupper($sql), "DELETE") !== false) {
            return "DELETE";
        }
        return "unknown";
    }

    protected function runQuery($sql, $assoc = true) {

        $this->resultData = [];

        if (!$assoc) {
            $assoc = false;
        }

        // run the query
        $result = $this->conn->query($sql);

        $queryType = $this->getQueryType($sql);

        // if successful
        if ($result) {
            // how many rows were affected
            $this->affectedRows = mysqli_affected_rows($this->conn);

            // select queries need to return data so
            // we save the data in an instance variable
            if ($queryType == "SELECT") {
                if (!$assoc) {
                    while ($row = $result->fetch_array()) {
                        if ($row) {
                            $this->resultData[] = $row;
                        }
                    }
                } else {
                    while ($row = $result->fetch_assoc()) {
                        if ($row) {
                            $this->resultData[] = $row;
                        }
                    }
                }
            }
            // query successful
            return true;
        }
        // query failed
        return false;
    }
}


if (!debug_backtrace()) {

    $config = file_get_contents(".config.json");
    $config = json_decode($config,true);

    $host = $config['host'];
    $user = $config['user'];
    $passwd = $config['passwd'];
    $database = $config['database'];
    $temp = new MysqlCnx($host, $user, $passwd, $database);


    $sql = "DROP TABLE tuts";
    $resp = $temp->query($sql);
    print_r($resp);


    $sql = "CREATE TABLE tuts( ".
    "id INT NOT NULL AUTO_INCREMENT, ".
    "title VARCHAR(100) NOT NULL, ".
    "author VARCHAR(40) NOT NULL, ".
    "submission_date DATE, ".
    "PRIMARY KEY ( id )); ";

    $resp = $temp->query($sql);
    print_r($resp);



    $sql = "INSERT INTO tuts (`title`, `author`, `submission_date`)
            VALUES('Learn PHP', 'Paul Hader Prescott', NOW())";
            
    $temp->query($sql);
    print_r($resp);

    $sql = "INSERT INTO tuts (`title`, `author`, `submission_date`)
            VALUES('Learn MySQL', 'Ramesh Tableu', NOW())";
    $temp->query($sql);
    print_r($resp);
    
    $sql = "INSERT INTO tuts (`title`, `author`, `submission_date`)
            VALUES('Learn Python', 'Bell Constrictor', NOW())";
    $temp->query($sql);
    print_r($resp);
 


}
