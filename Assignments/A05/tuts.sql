
--
-- Table structure for table `tuts`
--

CREATE TABLE `tuts` (
  `id` int NOT NULL,
  `title` varchar(100) NOT NULL,
  `author` varchar(40) NOT NULL,
  `submission_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tuts`
--

INSERT INTO `tuts` (`id`, `title`, `author`, `submission_date`) VALUES
(1, 'Learn PHP', 'Paul Hader Prescott', '2021-09-01'),
(2, 'Learn MySQL', 'Ramesh Tableu', '2021-09-01'),
(3, 'Learn Python', 'Bell Constrictor', '2021-09-01'),
(4, 'whocares', 'griffin', '2021-09-14'),
(5, 'Learn Python Fast API', 'Loic', '2021-11-14'),
(6, 'Learn Pydantic', 'Leila', '2021-11-15'),
(7, 'Compensating for Pofessionals', 'Lord Shrek', '2021-11-22');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tuts`
--
ALTER TABLE `tuts`
  ADD PRIMARY KEY (`id`);

