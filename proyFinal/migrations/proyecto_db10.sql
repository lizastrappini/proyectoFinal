-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Servidor: db
-- Tiempo de generación: 02-08-2025 a las 03:24:24
-- Versión del servidor: 9.3.0
-- Versión de PHP: 8.2.27


SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `Notificacion`;
DROP TABLE IF EXISTS `Evento`;
DROP TABLE IF EXISTS `Pago`;
DROP TABLE IF EXISTS `Calendario`;
DROP TABLE IF EXISTS `Usuario`;
DROP TABLE IF EXISTS `migrations_applied`;
DROP TABLE IF EXISTS `Contacto`;

SET FOREIGN_KEY_CHECKS = 1;


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
-- Table structure for table `Contacto`
--

CREATE TABLE `Contacto` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Titulo` varchar(50) NOT NULL,
  `Valor` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Contacto`
--

INSERT INTO `Contacto` (`Id`, `Titulo`, `Valor`) VALUES
(1, 'Email', 'voley@rosariocentral.com'),
(2, 'WhatsApp', '+54 9 341 555-5678'),
(3, 'Instagram', 'https://www.instagram.com/voleycarc?igsh=MTZ0aHpiMDJmNTdnNg%3D%3D&utm_source=qr'),
(4, 'Teléfono', '+54 341 555-1234');


--
-- Estructura de tabla para la tabla `Calendario`
--

CREATE TABLE `Calendario` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `TipoEvento` varchar(255) NOT NULL,
  `FechaInicio` date NOT NULL,
  `FechaFin` date NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Evento`
--

CREATE TABLE `Evento` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Titulo` varchar(50) NOT NULL,
  `Descripcion` varchar(100) NOT NULL,
  `FechaInicio` datetime NOT NULL,
  `FechaFin` datetime NOT NULL,
  `TodoElDia` tinyint(1) NOT NULL,
  `Localidad` varchar(50) DEFAULT NULL,
  `IdTipoEvento` int NOT NULL,
  `IdCategoria` int NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `Evento`
--

INSERT INTO `Evento` (`Id`, `Titulo`, `Descripcion`, `FechaInicio`, `FechaFin`, `TodoElDia`, `Localidad`, `IdTipoEvento`, `IdCategoria`) VALUES
(1, 'Partido vs NOB', '', '2025-07-17 21:00:00', '2025-07-17 21:00:00', 0, 'Rosario', 2, 5),
(2, 'Venta de pizzas', '', '2025-08-20 11:00:00', '2025-08-20 14:00:00', 1, 'Rosario', 6, 7),
(3, 'Venta de pizzas', '', '2025-07-24 12:00:00', '2025-07-26 12:00:00', 1, 'Rosario', 6, 3),
(4, 'Suspension entrenamiento', 'feriado', '2025-07-03 20:00:00', '2025-07-03 21:00:00', 1, 'Rosario', 4, 5),
(5, 'Partido ', '', '2025-07-20 12:00:00', '2025-07-20 16:00:00', 0, '', 2, 4);

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
('Usuario5.sql', '2025-07-09 22:35:36'),
('proyecto_db7.sql', '2025-08-02 02:01:58'),
('proyecto_db8.sql', '2025-08-02 02:01:59'),
('proyecto_db9.sql', '2025-08-02 02:01:59');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Notificacion`
--

CREATE TABLE `Notificacion` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Titulo` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `IdCategoria` int DEFAULT NULL,
    PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `Notificacion`
--

INSERT INTO `Notificacion` (`Id`, `Descripcion`, `Titulo`, `IdCategoria`) VALUES
(2, 'prueba', 'prueba', NULL),
(3, 'hola esta es otra prueba para todos los usuarios', 'prueba 2', NULL),
(5, 'prueba ', 'Entrenamiento', NULL),
(9, 'prueba', 'Entrenamiento', 7),
(10, 'mensaje general', 'Partido Sub 18', NULL),
(11, 'mensaje para cat 18', 'Partido Sub 18', 5),
(12, 'mensaje solo para la cat sub 21', 'Partido', 6),
(13, 'prueba envio de emails', 'Entrenamiento', 6),
(14, 'Envio de emails a todos los usuarios', 'Aviso importante', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Pago`
--

CREATE TABLE `Pago` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `FechaPago` datetime NOT NULL,
  `FechaVencimiento` datetime NOT NULL,
  `IdEstado` int DEFAULT NULL,
  `Importe` int NOT NULL,
  `IdUsuario` int DEFAULT NULL,
    PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `Pago`
--

INSERT INTO `Pago` (`Id`, `FechaPago`, `FechaVencimiento`, `IdEstado`, `Importe`, `IdUsuario`) VALUES
(3, '2025-07-28 00:00:00', '2025-07-31 00:00:00', 1, 17000, 3),
(4, '2025-08-01 00:00:00', '2025-08-06 00:00:00', 1, 17000, 3),
(5, '2025-07-27 00:00:00', '2025-07-31 00:00:00', 2, 17000, 30),
(6, '2025-07-27 00:00:00', '2025-07-29 00:00:00', 3, 17000, 3),
(7, '2025-08-06 00:00:00', '2025-08-09 00:00:00', 3, 1600, 30),
(8, '2025-07-29 00:00:00', '2025-08-01 00:00:00', 2, 2400, 3),
(9, '2025-07-24 00:00:00', '2025-07-09 00:00:00', 1, 18000, 32),
(10, '2025-08-03 00:00:00', '2025-08-03 00:00:00', 2, 8500, 30);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Usuario`
--

CREATE TABLE `Usuario` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) NOT NULL,
  `Apellido` varchar(50) NOT NULL,
  `Dni` int NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `NombreUsuario` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `IdCategoria` int NOT NULL,
  `Localidad` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IdEstado` int NOT NULL,
  `Direccion` varchar(50) NOT NULL,
  `Telefono` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IdRol` int NOT NULL,
  `Token` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TokenEnviado` tinyint(1) NOT NULL,
  `FechaVencimientoToken` datetime DEFAULT NULL,
  `IdRama` int DEFAULT NULL,
  `IdDivision` int DEFAULT NULL,
    PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `Usuario`
--

INSERT INTO `Usuario` (`Id`, `Nombre`, `Apellido`, `Dni`, `Email`, `Password`, `NombreUsuario`, `IdCategoria`, `Localidad`, `IdEstado`, `Direccion`, `Telefono`, `IdRol`, `Token`, `TokenEnviado`, `FechaVencimientoToken`, `IdRama`, `IdDivision`) VALUES
(1, 'Lizaaa', 'Strappini 123', 41906554, 'lizastrappini99@gmail.com', 'scrypt:32768:8:1$1RQqZoiuA5Jhk8l9$c0ba9bb7977dbced95d5ce702c9436be419c46c0b5ede63b338a88845dd5ec5a4d7265efb8201d5d73a8a68ce6efad35de1186f670dd6f176d45849a2a9b9b9a', 'lizast99', 2, '1', 1, '3 de febrero 1026', '3471630099', 3, NULL, 0, NULL, 0, 0),
(3, 'Lara', 'Del Coro', 43124684, 'laradelcoro01@gmail.com', 'scrypt:32768:8:1$skZXySNsJhr5jHAC$bb2e25039ac655ac1ed634f698b2bdaa0b51c96559b843c57b696815f9921f5f6c32f8fb9577986774af5a667141ea62b125454076a3489bcfb41cde7e760094', 'lara123', 7, '1', 1, 'Maipu 123', '123456789', 2, 'dD1j0uw--OleIL8p2lGGYqosUTXElD5pbm7jLFGxWS4', 1, '2025-07-13 01:55:05', 2, 1),
(4, 'Mora', 'Kopech', 43491828, 'morakopech@gmail.com', 'scrypt:32768:8:1$skZXySNsJhr5jHAC$bb2e25039ac655ac1ed634f698b2bdaa0b51c96559b843c57b696815f9921f5f6c32f8fb9577986774af5a667141ea62b125454076a3489bcfb41cde7e760094', 'morakopech', 2, '1', 1, 'zeballos 123', '123456789', 1, 'rCXn_mbipXl_q-7RgVjAh7qPy84Adm5ZMJXkVf3iCTI', 1, '2025-07-28 23:33:48', 0, 0),
(28, 'Juan', 'Martinez', 10, 'laradelcoro01+1@gmail.com', 'scrypt:32768:8:1$kTyKA58Cb5HJc1hk$a6bb7be56bb040a3a88651e755debb9b5875d9b558747177bd1979b2814cedcb5ab4f12e70e4dee8827ee4fce63b6bf2bc8fe8a2f2da47cd3f91988d9d415ce7', 'entrenador_10', 6, '1', 1, 'N/A', '03471607768', 3, NULL, 0, NULL, 0, 0),
(30, 'Alan', 'Martinez', 1857295, 'laradelcoro01+3@gmail.com', 'scrypt:32768:8:1$yDBDGsdKWTzNHr3r$255eb0587dba694e454e56d9ff815c1f99ba3c3f9f61d1a470596e63f5786f9bf2c8d5714e2adff1e8605c21383f116b95efca19a611d9e44a62beb63614b5b4', 'entrenador_10', 1, '1', 1, 'N/A', '03471607768', 2, NULL, 0, NULL, 2, 2),
(31, 'Lara', 'Admin', 999999, 'laradelcoro01+admin@gmail.com', 'scrypt:32768:8:1$KMso2fhm7yeUgRvx$cbadff5ca677227e08acf6900fc2e146e1683223b3d2acee3020cde7a83925f702e7103e9b5ec008fe95e47fc25ace165de1e473747cf707467677cf0fc94e6a', 'lara_43124684', 2, '2', 1, 'prueba', '3471607768', 1, NULL, 0, NULL, 0, 0),
(32, 'Lara', 'Deportista', 55555555, 'laradelcoro01+deportista@gmail.com', 'scrypt:32768:8:1$frTvzxvpmjIgfqJ6$3766aeb21ee22476392e2da0afb79f51c3b821e14b834f57ca87e751e42ce6b378f6ca3c384018b5e606dbcafd9277f509fefc27320d6e3ce0a59d3393e0d43f', 'entrenador_55555555', 6, '2', 1, 'N/A', '03471607768', 2, NULL, 0, NULL, 1, 1),
(33, 'Lara', 'Entrenador', 7777777, 'laradelcoro01+entrenador@gmail.com', 'scrypt:32768:8:1$hGsGyWQJeiTKgDXn$d6633826fb5558962bae6d6a3a927cd7f00986b84af880d6c4c68b8171574cda1ece271ac2ce3e18f0615e1646ba766e6289299667b0cdda78bcf82b09cff5f7', 'entrenador_7777777', 4, '1', 1, 'N/A', '03471607768', 3, NULL, 0, NULL, 0, 0),
(36, 'Alan', 'Martinez', 101, 'laradelcoro01+33@gmail.com', 'scrypt:32768:8:1$bQILCuCPYRxNCWvj$a0f5934e33ce9df6f30e3e0b84b636bac3e86383d95f25420093e3147d19b926e9061bc75b2510db62ed1fa3bc7a1a89a42b311c84859c12f486b76169ba9849', 'entrenador_101', 3, '1', 1, 'N/A', '03471607768', 2, NULL, 0, NULL, 1, 2),
(37, 'Julian', 'Carlos', 105, 'laradelcoro01+13@gmail.com', 'scrypt:32768:8:1$ghmtx6HR4ccDTbP7$39bc3d06be038c51488ca2a3ce3ad5f24501d64cd190d9f386ceff51be6c4c29133ee73c34907fefa08f7e68c13b20e2fbefeffc49c13f08496b331c53fe70ca', 'entrenador_105', 3, '1', 1, 'N/A', '03471607768', 3, NULL, 0, NULL, 0, 0),
(39, 'Alan', 'Martinez', 1088, 'laradelcoro01+339@gmail.com', 'scrypt:32768:8:1$qDRTVFEVm6aYYStv$fe63ee97092023cf4df2ce9aa0bbdf48877d56b4b5a50e4c4a0750bb3a6acbecea15422c4d73e5e6d2ff8341e72ecb027ac37d43e28dc9be425e52f69ef75be7', 'entrenador_1088', 2, '1', 1, 'N/A', '03471607768', 2, NULL, 0, NULL, 1, 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `Usuario`
--
ALTER TABLE `Usuario`
  ADD UNIQUE KEY `Id` (`Id`),
  ADD UNIQUE KEY `Dni` (`Dni`),
  ADD UNIQUE KEY `Email` (`Email`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
