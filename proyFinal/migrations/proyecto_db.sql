-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Servidor: db
-- Tiempo de generación: 09-07-2025 a las 22:37:09
-- Versión del servidor: 9.3.0
-- Versión de PHP: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyecto_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `migrations_applied`
--

CREATE TABLE `migrations_applied` (
  `filename` varchar(255) NOT NULL,
  `applied_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `migrations_applied`
--

INSERT INTO `migrations_applied` (`filename`, `applied_at`) VALUES
('Usuario.sql', '2025-07-09 22:25:52'),
('Usuario2.sql', '2025-07-09 22:30:04'),
('Usuario3.sql', '2025-07-09 22:31:09'),
('Usuario4.sql', '2025-07-09 22:34:35'),
('Usuario5.sql', '2025-07-09 22:35:36');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Pago`
--

CREATE TABLE `Pago` (
  `Id` int NOT NULL,
  `FechaPago` datetime DEFAULT NULL,
  `FechaVencimiento` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Usuario`
--

CREATE TABLE `Usuario` (
  `Id` int NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Apellido` varchar(50) NOT NULL,
  `Dni` int NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL,
  `NombreUsuario` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `IdCategoria` int NOT NULL,
  `IdLocalidad` int NOT NULL,
  `IdEstado` int NOT NULL,
  `Direccion` varchar(50) NOT NULL,
  `Telefono` varchar(50) NOT NULL,
  `IdRol` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `Usuario`
--

INSERT INTO `Usuario` (`Id`, `Nombre`, `Apellido`, `Dni`, `Email`, `Password`, `NombreUsuario`, `IdCategoria`, `IdLocalidad`, `IdEstado`, `Direccion`, `Telefono`, `IdRol`) VALUES
(1, 'Liza', 'Strappini 123', 41906554, 'liza@gmail.com', 'liza123', 'lizast99', 2, 1, 2, '3 de febrero 1026', '3471630099', 4),
(3, 'Lara', 'Del Coro', 123456, 'lara@gmail.com', 'lara123', 'lara123', 7, 1, 2, 'Maipu 123', '123456789', 2),
(4, 'Mora', 'Kopech', 123456, 'mora@gmail.com', 'mora123', 'morakopech', 2, 1, 2, 'zeballos 123', '123456789', 4),
(5, 'otro', 'otro', 123456, 'otro@gmail.com', 'otro123', 'otro', 2, 1, 2, 'otro 123', '123456789', 4);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `migrations_applied`
--
ALTER TABLE `migrations_applied`
  ADD PRIMARY KEY (`filename`);

--
-- Indices de la tabla `Pago`
--
ALTER TABLE `Pago`
  ADD PRIMARY KEY (`Id`);

--
-- Indices de la tabla `Usuario`
--
ALTER TABLE `Usuario`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `Pago`
--
ALTER TABLE `Pago`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `Usuario`
--
ALTER TABLE `Usuario`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
