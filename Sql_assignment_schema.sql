-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 11, 2015 at 09:58 AM
-- Server version: 5.5.46-0ubuntu0.14.04.2
-- PHP Version: 5.6.13-1+deb.sury.org~trusty+3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `flight_data`
--

-- --------------------------------------------------------

--
-- Table structure for table `aircraft`
--

CREATE TABLE IF NOT EXISTS `aircraft` (
  `acno` varchar(10) NOT NULL,
  `type` varchar(10) NOT NULL,
  `capacity` int(3) NOT NULL,
  `pilots` int(3) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `aircraft`
--

INSERT INTO `aircraft` (`acno`, `type`, `capacity`, `pilots`) VALUES
('N173WY', 'C-172', 3, 1),
('N35A', 'B-18', 9, 2),
('N412B ', 'DC-3', 21, 2),
('N747UA', 'B-747', 300, 3);

-- --------------------------------------------------------

--
-- Table structure for table `aircraft_assignments`
--

CREATE TABLE IF NOT EXISTS `aircraft_assignments` (
  `acno` varchar(10) NOT NULL,
  `fltno` int(5) NOT NULL,
  `date` varchar(5) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `aircraft_assignments`
--

INSERT INTO `aircraft_assignments` (`acno`, `fltno`, `date`) VALUES
('N35A', 1, '4-1'),
('N173WY', 2, '4-1'),
('N412B ', 3, '4-1'),
('N35A', 4, '4-1'),
('N173WY', 5, '4-1'),
('N412B ', 6, '4-2'),
('N173WY', 1, '4-2'),
('N35A', 2, '4-2'),
('N747UA', 3, '4-2'),
('N173WY', 4, '4-2'),
('N35A', 5, '4-2');

-- --------------------------------------------------------

--
-- Table structure for table `flights`
--

CREATE TABLE IF NOT EXISTS `flights` (
  `fltno` int(11) NOT NULL,
  `date` varchar(5) NOT NULL,
  `origin` varchar(4) NOT NULL,
  `destination` varchar(4) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `flights`
--

INSERT INTO `flights` (`fltno`, `date`, `origin`, `destination`) VALUES
(1, '4-1', 'DFW', 'DIA'),
(2, '4-1', 'DFW', 'ORD'),
(3, '4-1', 'DFW', 'LAX'),
(4, '4-1', 'DIA', 'DFW'),
(5, '4-1', 'ORD', 'DFW'),
(6, '4-2', 'LAX', 'DFW'),
(1, '4-2', 'DFW', 'DIA'),
(2, '4-2', 'DFW', 'ORD'),
(3, '4-2', 'DFW', 'LAX'),
(4, '4-2', 'DIA', 'DFW'),
(5, '4-2', 'ORD', 'DFW');

-- --------------------------------------------------------

--
-- Table structure for table `passengers`
--

CREATE TABLE IF NOT EXISTS `passengers` (
  `passid` int(4) NOT NULL,
  `name` varchar(25) NOT NULL,
  PRIMARY KEY (`passid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `passengers`
--

INSERT INTO `passengers` (`passid`, `name`) VALUES
(1001, 'Simpson, Richard'),
(1002, 'Halverson, Ranette'),
(1003, 'Carpenter, Stewart'),
(1004, 'Griffin, Terry'),
(1005, 'Hinds, Bill'),
(1101, 'Mouse, Mickey'),
(1102, 'Duck, Donald'),
(1103, 'Bunny, Bugs'),
(1104, 'Moose, Bullwinkle'),
(1105, 'Fudd, Elmer'),
(1011, 'Wayne, John'),
(1012, 'Mazurki, Mike'),
(1013, 'Marvin, Lee'),
(1014, 'Romero, Cesar'),
(1015, 'Lamour, Dorothy');

-- --------------------------------------------------------

--
-- Table structure for table `pass_ticketed`
--

CREATE TABLE IF NOT EXISTS `pass_ticketed` (
  `passid` int(5) NOT NULL,
  `fltno` int(5) NOT NULL,
  `date` varchar(5) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pass_ticketed`
--

INSERT INTO `pass_ticketed` (`passid`, `fltno`, `date`) VALUES
(1001, 1, '4-1'),
(1002, 1, '4-1'),
(1003, 2, '4-1'),
(1004, 1, '4-1'),
(1005, 2, '4-1'),
(1101, 2, '4-1'),
(1102, 3, '4-1'),
(1103, 1, '4-1'),
(1104, 2, '4-1'),
(1105, 2, '4-1'),
(1011, 3, '4-1'),
(1012, 3, '4-1'),
(1013, 3, '4-1'),
(1014, 3, '4-1'),
(1015, 3, '4-1'),
(1001, 4, '4-2'),
(1002, 4, '4-2'),
(1101, 5, '4-2'),
(1104, 5, '4-2'),
(1011, 6, '4-2'),
(1012, 6, '4-2'),
(1013, 6, '4-2'),
(1001, 2, '4-1'),
(1003, 1, '4-1'),
(1102, 5, '4-1'),
(1011, 4, '4-1'),
(1013, 5, '4-1'),
(1015, 5, '4-1');

-- --------------------------------------------------------

--
-- Table structure for table `pilots`
--

CREATE TABLE IF NOT EXISTS `pilots` (
  `pilotid` int(5) NOT NULL,
  `name` varchar(25) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pilots`
--

INSERT INTO `pilots` (`pilotid`, `name`) VALUES
(1030, 'Wright, Orville'),
(2137, 'Lindergh, Charles'),
(241, 'Yeager, Chuck'),
(7305, 'Post, Wiley'),
(2033, 'Boyington, Greg'),
(4315, 'Lovell, James'),
(3102, 'Hoover, Bob'),
(29, 'Wittman. Steve');

-- --------------------------------------------------------

--
-- Table structure for table `pilot_assignments`
--

CREATE TABLE IF NOT EXISTS `pilot_assignments` (
  `pilotid` int(5) NOT NULL,
  `fltno` int(5) NOT NULL,
  `date` varchar(5) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pilot_assignments`
--

INSERT INTO `pilot_assignments` (`pilotid`, `fltno`, `date`) VALUES
(1030, 1, '4-1'),
(7305, 1, '4-1'),
(2137, 2, '4-1'),
(241, 3, '4-1'),
(1030, 4, '4-1'),
(7305, 4, '4-1'),
(2137, 5, '4-1'),
(241, 6, '4-2'),
(1030, 1, '4-2'),
(4315, 2, '4-2'),
(29, 2, '4-2'),
(2033, 3, '4-2'),
(3102, 3, '4-2'),
(7305, 4, '4-2'),
(4315, 5, '4-2'),
(29, 5, '4-2');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
