
CREATE USER 'diekhoff'@'%' IDENTIFIED WITH mysql_native_password AS '';
CREATE DATABASE IF NOT EXISTS `diekhoff`;
GRANT ALL PRIVILEGES ON `diekhoff`.* TO 'diekhoff'@'%';