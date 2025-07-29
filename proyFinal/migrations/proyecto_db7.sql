-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: Jul 29, 2025 at 12:08 AM
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
('proyecto_db5.sql', '2025-07-27 20:14:29'),
('proyecto_db6.sql', '2025-07-28 17:37:34'),
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
  `FechaPago` datetime NOT NULL,
  `FechaVencimiento` datetime NOT NULL,
  `Estado` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Importe` int NOT NULL,
  `Usuario_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Pago`
--

INSERT INTO `Pago` (`Id`, `FechaPago`, `FechaVencimiento`, `Estado`, `Importe`, `Usuario_id`) VALUES
(3, '2025-07-28 00:00:00', '2025-07-31 00:00:00', '1', 17000, 3),
(4, '2025-08-01 00:00:00', '2025-08-06 00:00:00', '1', 17000, 3),
(5, '2025-07-27 00:00:00', '2025-07-31 00:00:00', '2', 17000, 30),
(6, '2025-07-27 00:00:00', '2025-07-29 00:00:00', '3', 17000, 3),
(7, '2025-08-06 00:00:00', '2025-08-09 00:00:00', '3', 1600, 30),
(8, '2025-07-29 00:00:00', '2025-08-01 00:00:00', '2', 2400, 3);

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
  `Telefono` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IdRol` int NOT NULL,
  `Token` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TokenEnviado` tinyint(1) NOT NULL,
  `FechaVencimientoToken` datetime DEFAULT NULL,
  `Rama` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Division` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Usuario`
--

INSERT INTO `Usuario` (`Id`, `Nombre`, `Apellido`, `Dni`, `Email`, `Password`, `NombreUsuario`, `Categoria`, `IdLocalidad`, `IdEstado`, `Direccion`, `Telefono`, `IdRol`, `Token`, `TokenEnviado`, `FechaVencimientoToken`, `Rama`, `Division`) VALUES
(1, 'Lizaaa', 'Strappini 123', 41906554, 'lizastrappini99@gmail.com', 'scrypt:32768:8:1$skZXySNsJhr5jHAC$bb2e25039ac655ac1ed634f698b2bdaa0b51c96559b843c57b696815f9921f5f6c32f8fb9577986774af5a667141ea62b125454076a3489bcfb41cde7e760094', 'lizast99', '2', 1, '1', '3 de febrero 1026', '3471630099', 3, NULL, 0, NULL, '', ''),
(3, 'Lara', 'Del Coro', 43124684, 'laradelcoro01@gmail.com', 'scrypt:32768:8:1$skZXySNsJhr5jHAC$bb2e25039ac655ac1ed634f698b2bdaa0b51c96559b843c57b696815f9921f5f6c32f8fb9577986774af5a667141ea62b125454076a3489bcfb41cde7e760094', 'lara123', '7', 1, '1', 'Maipu 123', '123456789', 2, 'dD1j0uw--OleIL8p2lGGYqosUTXElD5pbm7jLFGxWS4', 1, '2025-07-13 01:55:05', '2', '1'),
(4, 'Mora', 'Kopech', 43491828, 'morakopech@gmail.com', 'scrypt:32768:8:1$skZXySNsJhr5jHAC$bb2e25039ac655ac1ed634f698b2bdaa0b51c96559b843c57b696815f9921f5f6c32f8fb9577986774af5a667141ea62b125454076a3489bcfb41cde7e760094', 'morakopech', '2', 1, '1', 'zeballos 123', '123456789', 1, 'rCXn_mbipXl_q-7RgVjAh7qPy84Adm5ZMJXkVf3iCTI', 1, '2025-07-28 23:33:48', '', ''),
(28, 'Juan', 'Martinez', 10, 'laradelcoro01+1@gmail.com', 'scrypt:32768:8:1$kTyKA58Cb5HJc1hk$a6bb7be56bb040a3a88651e755debb9b5875d9b558747177bd1979b2814cedcb5ab4f12e70e4dee8827ee4fce63b6bf2bc8fe8a2f2da47cd3f91988d9d415ce7', 'entrenador_10', '6', 1, '1', 'N/A', '03471607768', 3, NULL, 0, NULL, '', ''),
(30, 'Alan', 'Martinez', 10, 'laradelcoro01+3@gmail.com', 'scrypt:32768:8:1$yDBDGsdKWTzNHr3r$255eb0587dba694e454e56d9ff815c1f99ba3c3f9f61d1a470596e63f5786f9bf2c8d5714e2adff1e8605c21383f116b95efca19a611d9e44a62beb63614b5b4', 'entrenador_10', '1', 1, '1', 'N/A', '03471607768', 2, NULL, 0, NULL, '2', '2'),
(31, 'Lara', 'Admin', 999999, 'laradelcoro01+admin@gmail.com', 'scrypt:32768:8:1$KMso2fhm7yeUgRvx$cbadff5ca677227e08acf6900fc2e146e1683223b3d2acee3020cde7a83925f702e7103e9b5ec008fe95e47fc25ace165de1e473747cf707467677cf0fc94e6a', 'lara_43124684', '', 1, '1', 'prueba', '3471607768', 1, NULL, 0, NULL, '', ''),
(32, 'Lara', 'Deportista', 55555555, 'laradelcoro01+deportista@gmail.com', 'scrypt:32768:8:1$frTvzxvpmjIgfqJ6$3766aeb21ee22476392e2da0afb79f51c3b821e14b834f57ca87e751e42ce6b378f6ca3c384018b5e606dbcafd9277f509fefc27320d6e3ce0a59d3393e0d43f', 'entrenador_55555555', '6', 1, '1', 'N/A', '03471607768', 2, NULL, 0, NULL, '1', '1'),
(33, 'Lara', 'Entrenador', 7777777, 'laradelcoro01+entrenador@gmail.com', 'scrypt:32768:8:1$hGsGyWQJeiTKgDXn$d6633826fb5558962bae6d6a3a927cd7f00986b84af880d6c4c68b8171574cda1ece271ac2ce3e18f0615e1646ba766e6289299667b0cdda78bcf82b09cff5f7', 'entrenador_7777777', '4', 1, '1', 'N/A', '03471607768', 3, NULL, 0, NULL, NULL, NULL);

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
-- Indexes for table `Pago`
--
ALTER TABLE `Pago`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `fk_pago_usuario` (`Usuario_id`);

--
-- Indexes for table `Usuario`
--
ALTER TABLE `Usuario`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Pago`
--
ALTER TABLE `Pago`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `Usuario`
--
ALTER TABLE `Usuario`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Pago`
--
ALTER TABLE `Pago`
  ADD CONSTRAINT `fk_pago_usuario` FOREIGN KEY (`Usuario_id`) REFERENCES `Usuario` (`Id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
