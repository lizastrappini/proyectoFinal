-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: Jul 27, 2025 at 03:24 AM
-- Server version: 9.3.0
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `proyecto_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `Calendario`
--

CREATE TABLE `Calendario` (
  `Id` int NOT NULL,
  `TipoEvento` varchar(255) NOT NULL,
  `FechaInicio` date NOT NULL,
  `FechaFin` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Evento`
--

CREATE TABLE `Evento` (
  `Id` int NOT NULL,
  `Titulo` varchar(50) NOT NULL,
  `Descripcion` varchar(100) NOT NULL,
  `FechaInicio` datetime NOT NULL,
  `FechaFin` datetime NOT NULL,
  `TodoElDia` tinyint(1) NOT NULL,
  `Localidad` varchar(50) DEFAULT NULL,
  `TipoEvento` int NOT NULL,
  `Categoria` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Evento`
--

INSERT INTO `Evento` (`Id`, `Titulo`, `Descripcion`, `FechaInicio`, `FechaFin`, `TodoElDia`, `Localidad`, `TipoEvento`, `Categoria`) VALUES
(1, 'Partido vs NOB', '', '2025-07-17 21:00:00', '2025-07-17 21:00:00', 0, 'Rosario', 2, '5'),
(2, 'Venta de pizzas', '', '2025-08-20 11:00:00', '2025-08-20 14:00:00', 1, 'Rosario', 6, '7'),
(3, 'Venta de pizzas', '', '2025-07-24 12:00:00', '2025-07-26 12:00:00', 1, 'Rosario', 6, '3'),
(4, 'Suspension entrenamiento', 'feriado', '2025-07-03 20:00:00', '2025-07-03 21:00:00', 1, 'Rosario', 4, '5'),
(5, 'Partido ', '', '2025-07-20 12:00:00', '2025-07-20 16:00:00', 0, '', 2, '4');

-- --------------------------------------------------------

--
-- Table structure for table `migrations_applied`
--

CREATE TABLE `migrations_applied` (
  `filename` varchar(255) NOT NULL,
  `applied_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `migrations_applied`
--

INSERT INTO `migrations_applied` (`filename`, `applied_at`) VALUES
('proyecto_db.sql', '2025-07-09 22:37:41'),
('proyecto_db1.sql', '2025-07-13 14:43:20'),
('proyecto_db2.sql', '2025-07-09 22:49:37'),
('proyecto_db3.sql', '2025-07-11 21:24:08'),
('proyecto_db4.sql', '2025-07-17 21:29:24'),
('Usuario.sql', '2025-07-09 22:25:52'),
('Usuario2.sql', '2025-07-09 22:30:04'),
('Usuario3.sql', '2025-07-09 22:31:09'),
('Usuario4.sql', '2025-07-09 22:34:35'),
('Usuario5.sql', '2025-07-09 22:35:36');

-- --------------------------------------------------------

--
-- Table structure for table `Notificacion`
--

CREATE TABLE `Notificacion` (
  `Id` int NOT NULL,
  `FechaInicio` date NOT NULL,
  `FechaFin` date NOT NULL,
  `Descripcion` text NOT NULL,
  `Titulo` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Pago`
--

CREATE TABLE `Pago` (
  `Id` int NOT NULL,
  `FechaPago` datetime DEFAULT NULL,
  `FechaVencimiento` datetime NOT NULL,
  `Estado` tinyint(1) DEFAULT NULL,
  `Importe` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Usuario`
--

CREATE TABLE `Usuario` (
  `Id` int NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Apellido` varchar(50) NOT NULL,
  `Dni` int NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `NombreUsuario` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Categoria` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `IdLocalidad` int NOT NULL,
  `IdEstado` varchar(10) NOT NULL,
  `Direccion` varchar(50) NOT NULL,
  `Telefono` varchar(50) NOT NULL,
  `IdRol` int NOT NULL,
  `Token` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TokenEnviado` tinyint(1) NOT NULL,
  `FechaVencimientoToken` datetime DEFAULT NULL,
  `Rama` varchar(50) NOT NULL,
  `Division` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Usuario`
--

INSERT INTO `Usuario` (`Id`, `Nombre`, `Apellido`, `Dni`, `Email`, `Password`, `NombreUsuario`, `Categoria`, `IdLocalidad`, `IdEstado`, `Direccion`, `Telefono`, `IdRol`, `Token`, `TokenEnviado`, `FechaVencimientoToken`, `Rama`, `Division`) VALUES
(1, 'Lizaaa', 'Strappini 123', 41906554, 'lizastrappini99@gmail.com', 'liza99', 'lizast99', '2', 1, '1', '3 de febrero 1026', '3471630099', 3, NULL, 0, NULL, '', ''),
(3, 'Lara', 'Del Coro', 43124684, 'laradelcoro01@gmail.com', 'lara123', 'lara123', '7', 1, '1', 'Maipu 123', '123456789', 2, 'dD1j0uw--OleIL8p2lGGYqosUTXElD5pbm7jLFGxWS4', 1, '2025-07-13 01:55:05', '2', '1'),
(4, 'Mora', 'Kopech', 123456, 'mora@gmail.com', 'mora1234', 'morakopech', '2', 1, '2', 'zeballos 123', '123456789', 1, NULL, 0, NULL, '', ''),
(28, 'Juan', 'Martinez', 10, 'laradelcoro01+1@gmail.com', 'password', 'entrenador_10', '6', 1, '1', 'N/A', '03471607768', 3, NULL, 0, NULL, '', ''),
(30, 'Alan', 'Martinez', 10, 'laradelcoro01+3@gmail.com', '12345678', 'entrenador_10', '1', 1, '1', 'N/A', '03471607768', 2, NULL, 0, NULL, '2', '2');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Calendario`
--
ALTER TABLE `Calendario`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `migrations_applied`
--
ALTER TABLE `migrations_applied`
  ADD PRIMARY KEY (`filename`);

--
-- Indexes for table `Notificacion`
--
ALTER TABLE `Notificacion`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `Usuario`
--
ALTER TABLE `Usuario`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Usuario`
--
ALTER TABLE `Usuario`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
