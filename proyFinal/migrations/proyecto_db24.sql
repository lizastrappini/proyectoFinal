-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Servidor: db
-- Tiempo de generación: 18-09-2025 a las 04:30:49
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
CREATE DATABASE IF NOT EXISTS `proyecto_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `proyecto_db`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Calendario`
--

DROP TABLE IF EXISTS `Calendario`;
CREATE TABLE `Calendario` (
  `Id` int NOT NULL,
  `TipoEvento` varchar(255) NOT NULL,
  `FechaInicio` date NOT NULL,
  `FechaFin` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Truncar tablas antes de insertar `Calendario`
--

TRUNCATE TABLE `Calendario`;
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Contacto`
--

DROP TABLE IF EXISTS `Contacto`;
CREATE TABLE `Contacto` (
  `Id` int NOT NULL,
  `Titulo` varchar(50) NOT NULL,
  `Valor` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `prueba` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Truncar tablas antes de insertar `Contacto`
--

TRUNCATE TABLE `Contacto`;
--
-- Volcado de datos para la tabla `Contacto`
--

INSERT INTO `Contacto` (`Id`, `Titulo`, `Valor`, `prueba`) VALUES
(1, 'Email', 'voley@rosariocentral.com', NULL),
(2, 'WhatsApp', '+54 9 341 555-5678', NULL),
(3, 'Instagram', 'https://www.instagram.com/voleycarc?igsh=MTZ0aHpiMDJmNTdnNg%3D%3D&utm_source=qr', NULL),
(4, 'Teléfono', '+54 341 555-1234', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `EstadisticaPorPartido`
--

DROP TABLE IF EXISTS `EstadisticaPorPartido`;
CREATE TABLE `EstadisticaPorPartido` (
  `Id` int NOT NULL,
  `IdPartido` int NOT NULL,
  `Fecha` datetime NOT NULL,
  `IdContrincante` int NOT NULL,
  `IdCategoria` int NOT NULL,
  `IdRama` int NOT NULL,
  `IdDivision` int NOT NULL,
  `Resultado` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Truncar tablas antes de insertar `EstadisticaPorPartido`
--

TRUNCATE TABLE `EstadisticaPorPartido`;
--
-- Volcado de datos para la tabla `EstadisticaPorPartido`
--

INSERT INTO `EstadisticaPorPartido` (`Id`, `IdPartido`, `Fecha`, `IdContrincante`, `IdCategoria`, `IdRama`, `IdDivision`, `Resultado`) VALUES
(13, 1, '2025-07-17 00:00:00', 2, 2, 1, 1, 1),
(14, 1, '2025-07-17 00:00:00', 2, 2, 1, 1, 1),
(15, 6, '2025-07-20 00:00:00', 1, 2, 1, 1, 2),
(16, 7, '2025-07-16 00:00:00', 4, 1, 1, 1, 2),
(17, 8, '2025-09-06 00:00:00', 3, 3, 1, 2, 1),
(18, 9, '2025-09-12 00:00:00', 1, 3, 2, 2, 1),
(19, 28, '2025-09-27 00:00:00', 4, 5, 2, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `EstadisticaUsuarioPartido`
--

DROP TABLE IF EXISTS `EstadisticaUsuarioPartido`;
CREATE TABLE `EstadisticaUsuarioPartido` (
  `Id` int NOT NULL,
  `IdEstadisticaPorPartido` int NOT NULL,
  `IdUsuario` int NOT NULL,
  `REE` int NOT NULL,
  `REV` int NOT NULL,
  `RE0` int NOT NULL,
  `RE1` int NOT NULL,
  `RE2` int NOT NULL,
  `RE3` int NOT NULL,
  `RETOTAL` int NOT NULL,
  `ROE` int NOT NULL,
  `ROB` int NOT NULL,
  `RO0` int NOT NULL,
  `RO1` int NOT NULL,
  `RO2` int NOT NULL,
  `RO3` int NOT NULL,
  `RO4` int NOT NULL,
  `ROTOTAL` int NOT NULL,
  `TRE` int NOT NULL,
  `TRB` int NOT NULL,
  `TR0` int NOT NULL,
  `TR1` int NOT NULL,
  `TR2` int NOT NULL,
  `TR3` int NOT NULL,
  `TR4` int NOT NULL,
  `TRTOTAL` int NOT NULL,
  `SA0` int NOT NULL,
  `SA1` int NOT NULL,
  `SA2` int NOT NULL,
  `SA3` int NOT NULL,
  `SA4` int NOT NULL,
  `SATOTAL` int NOT NULL,
  `BLP` int NOT NULL,
  `BLN` int NOT NULL,
  `BLTOTAL` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Truncar tablas antes de insertar `EstadisticaUsuarioPartido`
--

TRUNCATE TABLE `EstadisticaUsuarioPartido`;
--
-- Volcado de datos para la tabla `EstadisticaUsuarioPartido`
--

INSERT INTO `EstadisticaUsuarioPartido` (`Id`, `IdEstadisticaPorPartido`, `IdUsuario`, `REE`, `REV`, `RE0`, `RE1`, `RE2`, `RE3`, `RETOTAL`, `ROE`, `ROB`, `RO0`, `RO1`, `RO2`, `RO3`, `RO4`, `ROTOTAL`, `TRE`, `TRB`, `TR0`, `TR1`, `TR2`, `TR3`, `TR4`, `TRTOTAL`, `SA0`, `SA1`, `SA2`, `SA3`, `SA4`, `SATOTAL`, `BLP`, `BLN`, `BLTOTAL`) VALUES
(7, 13, 4, 1, 3, 4, 3, 3, 8, 20, 3, 3, 6, 2, 8, 15, 2, 33, 2, 1, 4, 2, 8, 3, 2, 19, 1, 3, 5, 2, 5, 16, 16, 18, 14),
(8, 14, 4, 1, 3, 4, 3, 3, 8, 18, 3, 3, 6, 2, 8, 15, 2, 33, 2, 1, 4, 2, 8, 3, 2, 19, 1, 3, 5, 2, 5, 16, 18, 14, 34),
(9, 15, 3, 1, 3, 4, 3, 3, 8, 18, 3, 3, 6, 2, 8, 15, 2, 33, 2, 1, 4, 2, 8, 3, 2, 19, 1, 3, 5, 2, 5, 16, 18, 14, 34),
(10, 15, 4, 1, 3, 4, 3, 3, 8, 18, 3, 3, 6, 2, 8, 15, 2, 33, 2, 1, 4, 2, 8, 3, 2, 19, 1, 3, 5, 2, 5, 16, 18, 14, 34),
(11, 16, 3, 1, 3, 4, 3, 3, 8, 18, 3, 3, 6, 2, 8, 15, 2, 33, 2, 1, 4, 2, 8, 3, 2, 19, 1, 3, 5, 2, 5, 16, 18, 14, 34),
(12, 17, 36, 1, 3, 4, 3, 3, 8, 18, 3, 3, 6, 2, 8, 15, 2, 33, 2, 1, 4, 2, 8, 3, 2, 19, 1, 3, 5, 2, 5, 16, 18, 14, 34),
(13, 18, 30, 1, 3, 4, 3, 3, 8, 18, 3, 3, 6, 2, 8, 15, 2, 33, 2, 1, 4, 2, 8, 3, 2, 19, 1, 3, 5, 2, 5, 16, 18, 14, 34),
(14, 19, 3, 1, 3, 4, 3, 3, 8, 18, 3, 3, 6, 2, 8, 15, 2, 33, 2, 1, 4, 2, 8, 3, 2, 19, 1, 3, 5, 2, 5, 16, 18, 14, 34),
(15, 19, 4, 1, 3, 4, 3, 3, 8, 18, 3, 3, 6, 2, 8, 15, 2, 33, 2, 1, 4, 2, 8, 3, 2, 19, 1, 3, 5, 2, 5, 16, 18, 14, 34),
(16, 19, 32, 1, 3, 4, 3, 3, 8, 18, 3, 3, 6, 2, 8, 15, 2, 33, 2, 1, 4, 2, 8, 3, 2, 19, 1, 3, 5, 2, 5, 16, 18, 14, 34);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Evento`
--

DROP TABLE IF EXISTS `Evento`;
CREATE TABLE `Evento` (
  `Id` int NOT NULL,
  `Titulo` varchar(50) NOT NULL,
  `Descripcion` varchar(100) NOT NULL,
  `FechaInicio` datetime NOT NULL,
  `FechaFin` datetime NOT NULL,
  `TodoElDia` tinyint(1) NOT NULL,
  `IdLocalidad` int DEFAULT NULL,
  `IdTipoEvento` int NOT NULL,
  `IdCategoria` int DEFAULT NULL,
  `IdRama` int DEFAULT NULL,
  `IdDivision` int DEFAULT NULL,
  `TieneEstadistica` tinyint(1) NOT NULL,
  `IdContrincante` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Truncar tablas antes de insertar `Evento`
--

TRUNCATE TABLE `Evento`;
--
-- Volcado de datos para la tabla `Evento`
--

INSERT INTO `Evento` (`Id`, `Titulo`, `Descripcion`, `FechaInicio`, `FechaFin`, `TodoElDia`, `IdLocalidad`, `IdTipoEvento`, `IdCategoria`, `IdRama`, `IdDivision`, `TieneEstadistica`, `IdContrincante`) VALUES
(1, 'Partido vs NOB', '', '2025-07-17 21:00:00', '2025-07-17 21:00:00', 0, 1, 2, 2, 1, 1, 1, 2),
(2, 'Venta de pizzas', '', '2025-08-20 11:00:00', '2025-08-20 14:00:00', 1, 1, 6, 7, NULL, NULL, 0, NULL),
(3, 'Venta de pizzas', '', '2025-07-24 12:00:00', '2025-07-26 12:00:00', 1, 2, 6, 3, NULL, NULL, 0, NULL),
(4, 'Suspension entrenamiento', 'feriado', '2025-07-03 20:00:00', '2025-07-03 21:00:00', 1, 3, 4, 5, NULL, NULL, 0, NULL),
(5, 'Partido ', '', '2025-07-20 12:00:00', '2025-07-20 16:00:00', 0, 4, 2, 4, NULL, NULL, 0, NULL),
(6, 'Partido vs Sonder', '', '2025-07-20 12:00:00', '2025-07-20 12:00:00', 0, 1, 2, 2, 1, 1, 1, 1),
(7, 'Partido vs NN3', '', '2025-07-16 12:00:00', '2025-07-16 12:00:00', 0, 1, 2, 1, 1, 1, 1, 4),
(8, 'Partido vs nautico', '', '2025-09-06 12:00:00', '2025-09-06 12:00:00', 0, 1, 2, 3, 1, 2, 1, 3),
(9, 'Partido Sub14 Masculino B vs Sonder', '', '2025-09-12 12:00:00', '2025-09-12 12:00:00', 0, 1, 2, 3, 2, 2, 1, 1),
(10, 'Venta de pizzas', 'test', '2025-09-18 12:00:00', '2025-09-18 12:00:00', 0, 1, 6, 5, NULL, NULL, 0, NULL),
(11, 'Suspension entrenamiento', '', '2025-09-23 12:00:00', '2025-09-23 12:01:00', 0, 1, 4, 6, NULL, NULL, 0, NULL),
(13, 'Torneo', '', '2025-09-26 12:00:00', '2025-09-28 12:00:00', 0, NULL, 5, 4, 2, 2, 0, NULL),
(14, 'Torneo Sub21 Femenino A', '', '2025-09-20 12:00:00', '2025-09-21 12:00:00', 0, NULL, 5, 6, 1, 1, 0, NULL),
(15, 'Torneo Sub16 Femenino B', '', '2025-09-01 12:00:00', '2025-09-02 12:00:00', 0, 8, 5, 4, 1, 2, 0, NULL),
(16, 'Torneo Sub12 Femenino B', '', '2025-08-04 12:00:00', '2025-08-05 12:00:00', 0, 7, 5, 1, 1, 2, 0, NULL),
(17, 'Venta de empanadas', '', '2025-09-25 15:00:00', '2025-09-25 15:01:00', 0, 1, 6, 3, NULL, NULL, 0, NULL),
(18, 'Entrenamiento Sub18 Femenino A', 'Evento creado masivamente', '2025-09-16 18:00:00', '2025-09-16 19:30:00', 0, NULL, 1, 5, 1, 1, 0, NULL),
(19, 'Entrenamiento Primera Femenino A', 'Evento creado masivamente', '2025-10-06 20:00:00', '2025-10-06 21:30:00', 0, NULL, 1, 7, 1, 1, 0, NULL),
(20, 'Entrenamiento Primera Femenino A', 'Evento creado masivamente', '2025-10-08 20:00:00', '2025-10-08 21:30:00', 0, NULL, 1, 7, 1, 1, 0, NULL),
(21, 'Entrenamiento Primera Femenino A', 'Evento creado masivamente', '2025-10-10 20:00:00', '2025-10-10 21:30:00', 0, NULL, 1, 7, 1, 1, 0, NULL),
(22, 'Entrenamiento Primera Femenino A', 'Evento creado masivamente', '2025-10-13 20:00:00', '2025-10-13 21:30:00', 0, NULL, 1, 7, 1, 1, 0, NULL),
(23, 'Entrenamiento Primera Femenino A', 'Evento creado masivamente', '2025-10-15 20:00:00', '2025-10-15 21:30:00', 0, NULL, 1, 7, 1, 1, 0, NULL),
(24, 'Entrenamiento Primera Femenino A', 'Evento creado masivamente', '2025-10-17 20:00:00', '2025-10-17 21:30:00', 0, NULL, 1, 7, 1, 1, 0, NULL),
(25, 'Vacaciones de invierno', '', '2025-09-15 12:00:00', '2025-09-18 12:00:00', 0, NULL, 3, NULL, NULL, NULL, 0, NULL),
(26, 'Entrenamiento Sub12 Femenino A', '', '2025-10-21 17:00:00', '2025-10-21 17:01:00', 0, NULL, 1, 1, 1, 1, 0, NULL),
(27, 'Entrenamiento Sub12 Masculino B', 'Evento creado masivamente', '2025-10-23 17:00:00', '2025-10-23 18:30:00', 0, NULL, 1, 1, 2, 2, 0, NULL),
(28, 'Partido Sub18 Masculino A vs Normal3', '', '2025-09-27 21:00:00', '2025-09-27 21:01:00', 0, 1, 2, 5, 2, 1, 1, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `faq`
--

DROP TABLE IF EXISTS `faq`;
CREATE TABLE `faq` (
  `Id` int NOT NULL,
  `Pregunta` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Respuesta` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PalabrasClave` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Tema` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Truncar tablas antes de insertar `faq`
--

TRUNCATE TABLE `faq`;
--
-- Dumping data for table `faq`
--

INSERT INTO `faq` (`Id`, `Pregunta`, `Respuesta`, `PalabrasClave`, `Tema`) VALUES
(1, '¿Cómo me registro en Voley App?', 'Solo los administradores pueden crear usuarios. Una vez creado, recibirás un mail con tus credenciales para iniciar sesión.', 'registro, alta', 'Usuario'),
(2, 'Olvidé mi contraseña, ¿qué hago?', 'Haz clic en “Recuperar contraseña” en la pantalla de login. Te enviaremos un correo con las instrucciones para restablecerla.', 'recuperar, olvide', 'Usuario'),
(3, '¿Qué funciones tiene un entrenador en la app?', 'Los entrenadores pueden ver sus deportistas asignados, estadísticas, notificaciones importantes y actualizar información de contacto.', 'entrenador, funcion', 'Entrenador'),
(4, '¿Dónde puedo ver los eventos?', 'Ingresa al módulo “Calendario” en el menú lateral. Allí podrás ver todos los eventos asignados a tu equipo.', 'calendario, evento, entrenamiento, partido', 'Calendario'),
(6, '¿Cómo puedo actualizar mis datos personales?', 'Ve a “Mi Cuenta” en el menú lateral. Allí puedes modificar tu nombre, apellido, correo y teléfono.', 'datos personales, mi cuenta ', 'Usuario'),
(8, '¿Quién puede ver las cuotas de los deportistas?', 'Solo los administradores tienen acceso a la sección de “Pagos” para ver y gestionar pagos de los deportistas. Para ver tus pagos ve a \"Mi Cuenta\"', 'cuota ', 'Cuota Deportiva'),
(9, '¿Cómo agrego o elimino deportistas ?', 'Solo los administradores pueden agregar o eliminar usuarios desde las secciones “Deportistas” o “Entrenadores”.', 'alta, deportistas, entrenadores, eliminar', 'Deportista'),
(10, '¿Dónde puedo ver mi información personal?', 'Ve a “Mi Cuenta” en el menú lateral. Allí puedes ver tus datos personales', 'cuenta, datos, personales', 'Usuario'),
(11, '¿Cómo cambio mi contraseña?', 'Puede cambiar su contraseña desde la sección \'Mi Cuenta\' del menú.', 'contraseña', 'Usuario'),
(12, '¿Cómo puedo ver mis pagos deportivos?', 'Puede ver sus pagos y el estado de los mismos desde la sección \'Mi Cuenta\' del menú.', 'pagos', 'Cuota Deportiva'),
(13, '¿Cómo puedo ver mis estadisticas?', 'Ve a “Ver Estadisticas” en el menú lateral. Allí pueden buscar las estadisticas del partido que quieras.', 'estadistica', 'Estadisticas'),
(14, '¿Dónde subo las estadisticas del partido?', 'Ve a “Cargar Estadisticas” en el menú lateral. Allí podrás descargar el excel con el la planilla y subirla completa.', 'planilla, excel', 'Estadisticas');
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `migrations_applied`
--

DROP TABLE IF EXISTS `migrations_applied`;
CREATE TABLE `migrations_applied` (
  `filename` varchar(255) NOT NULL,
  `applied_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Truncar tablas antes de insertar `migrations_applied`
--

TRUNCATE TABLE `migrations_applied`;
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
('proyecto_db9.sql', '2025-08-02 02:01:59'),
('proyecto_db10.sql', '2025-09-04 05:30:26'),
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
('proyecto_db9.sql', '2025-08-02 02:01:59'),
('proyecto_db11.sql', '2025-09-04 05:30:26'),
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
('proyecto_db9.sql', '2025-08-02 02:01:59'),
('proyecto_db10.sql', '2025-09-01 12:15:07'),
('proyecto_db11.sql', '2025-09-01 12:15:07'),
('proyecto_db12.sql', '2025-09-04 05:30:26');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Notificacion`
--

DROP TABLE IF EXISTS `Notificacion`;
CREATE TABLE `Notificacion` (
  `Id` int NOT NULL,
  `Descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Titulo` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `IdCategoria` int DEFAULT NULL,
  `IdDivision` int DEFAULT NULL,
  `IdRama` int DEFAULT NULL,
  `FechaEnvio` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Truncar tablas antes de insertar `Notificacion`
--

TRUNCATE TABLE `Notificacion`;
--
-- Volcado de datos para la tabla `Notificacion`
--

INSERT INTO `Notificacion` (`Id`, `Descripcion`, `Titulo`, `IdCategoria`, `IdDivision`, `IdRama`, `FechaEnvio`) VALUES
(2, 'prueba', 'prueba', 4, NULL, NULL, '2025-09-18 03:08:52'),
(3, 'hola esta es otra prueba para todos los usuarios', 'prueba 2', 5, NULL, NULL, '2025-09-18 03:08:52'),
(5, 'prueba ', 'Entrenamiento', NULL, NULL, NULL, '2025-09-18 03:08:52'),
(9, 'prueba', 'Entrenamiento', NULL, NULL, NULL, '2025-09-18 03:08:52'),
(10, 'mensaje general', 'Partido Sub 18', NULL, NULL, NULL, '2025-09-18 03:08:52'),
(11, 'mensaje para cat 18', 'Partido Sub 18', NULL, NULL, NULL, '2025-09-18 03:08:52'),
(12, 'mensaje solo para la cat sub 21', 'Partido', NULL, NULL, NULL, '2025-09-18 03:08:52'),
(13, 'prueba envio de emails', 'Entrenamiento', NULL, NULL, NULL, '2025-09-18 03:08:52'),
(14, 'Envio de emails a todos los usuarios', 'Aviso importante', NULL, NULL, NULL, '2025-09-18 03:08:52'),
(15, 'test', 'test', NULL, NULL, NULL, '2025-09-18 03:08:52'),
(16, 'test', 'test', NULL, NULL, NULL, '2025-09-18 03:08:52'),
(17, 'holaaaaaaaaa', 'Prueba', 3, 2, 2, '2025-09-18 00:24:04');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Pago`
--

DROP TABLE IF EXISTS `Pago`;
CREATE TABLE `Pago` (
  `Id` int NOT NULL,
  `FechaPago` datetime DEFAULT NULL,
  `FechaVencimiento` datetime NOT NULL,
  `IdEstado` int DEFAULT NULL,
  `Importe` int NOT NULL,
  `IdUsuario` int DEFAULT NULL,
  `Comprobante` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Truncar tablas antes de insertar `Pago`
--

TRUNCATE TABLE `Pago`;
--
-- Volcado de datos para la tabla `Pago`
--

INSERT INTO `Pago` (`Id`, `FechaPago`, `FechaVencimiento`, `IdEstado`, `Importe`, `IdUsuario`, `Comprobante`) VALUES
(3, '2025-09-17 22:14:58', '2025-08-01 00:00:00', 1, 17001, 3, NULL),
(4, '2025-09-17 09:49:58', '2025-08-06 00:00:00', 1, 17000, 3, NULL),
(5, '2025-07-27 00:00:00', '2025-07-31 00:00:00', 1, 17000, 30, NULL),
(6, NULL, '2025-07-29 00:00:00', 2, 17000, 3, NULL),
(7, '2025-09-17 10:07:25', '2025-08-09 00:00:00', 1, 1600, 30, 'uploads/comprobante_7_pngwing.com.png'),
(8, '2025-09-17 09:50:53', '2025-08-01 00:00:00', 1, 2400, 3, NULL),
(9, '2025-07-24 00:00:00', '2025-07-09 00:00:00', 1, 18000, 32, NULL),
(10, '2025-09-16 23:54:31', '2025-08-03 00:00:00', 1, 8500, 30, NULL),
(26, '2025-09-22 00:00:00', '2025-09-08 00:00:00', 2, 8501, 3, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Parametro`
--

DROP TABLE IF EXISTS `Parametro`;
CREATE TABLE `Parametro` (
  `Id` int NOT NULL,
  `Titulo` varchar(50) NOT NULL,
  `Valor` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Truncar tablas antes de insertar `Parametro`
--

TRUNCATE TABLE `Parametro`;
--
-- Volcado de datos para la tabla `Parametro`
--

INSERT INTO `Parametro` (`Id`, `Titulo`, `Valor`) VALUES
(1, 'Email', 'voley@rosariocentral.com'),
(2, 'WhatsApp', '+54 9 341 555-5678'),
(3, 'Instagram', 'https://www.instagram.com/voleycarc?igsh=MTZ0aHpiMDJmNTdnNg%3D%3D&utm_source=qr'),
(4, 'Teléfono', '+54 341 555-1234'),
(5, 'ValorCuota', '8501');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Usuario`
--

DROP TABLE IF EXISTS `Usuario`;
CREATE TABLE `Usuario` (
  `Id` int NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Apellido` varchar(50) NOT NULL,
  `Dni` int NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `NombreUsuario` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `IdCategoria` int NOT NULL,
  `Localidad` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IdEstado` int NOT NULL,
  `Direccion` varchar(50) DEFAULT NULL,
  `Telefono` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IdRol` int NOT NULL,
  `Token` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TokenEnviado` tinyint(1) NOT NULL,
  `FechaVencimientoToken` datetime DEFAULT NULL,
  `IdRama` int DEFAULT NULL,
  `IdDivision` int DEFAULT NULL,
  `FechaNacimiento` datetime DEFAULT NULL,
  `CategoriaExtra` varchar(10) DEFAULT NULL,
  `Federado` tinyint(1) NOT NULL DEFAULT '3'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Truncar tablas antes de insertar `Usuario`
--

TRUNCATE TABLE `Usuario`;
--
-- Volcado de datos para la tabla `Usuario`
--

INSERT INTO `Usuario` (`Id`, `Nombre`, `Apellido`, `Dni`, `Email`, `Password`, `NombreUsuario`, `IdCategoria`, `Localidad`, `IdEstado`, `Direccion`, `Telefono`, `IdRol`, `Token`, `TokenEnviado`, `FechaVencimientoToken`, `IdRama`, `IdDivision`, `FechaNacimiento`, `CategoriaExtra`, `Federado`) VALUES
(1, 'Liza', 'Strappini 123', 41906554, 'lizastrappini99@gmail.com', 'scrypt:32768:8:1$TkuXgqifo8KOANqD$031a85fab581addce10403ecdb7e3e95ce85bba8e240d3965ab1ac8f0f10a0c672a21f1d69a67145598f37651d81a63e2e79ec0081364eace5d2cb2ce1f9f6bb', 'lizast99', 1, '1', 1, '3 de febrero 1026', '3471630099', 1, NULL, 0, NULL, 1, 1, '2025-09-13 00:00:00', '7', 1),
(3, 'Lara', 'Del Coro', 43124684, 'laradelcoro01@gmail.com', 'scrypt:32768:8:1$skZXySNsJhr5jHAC$bb2e25039ac655ac1ed634f698b2bdaa0b51c96559b843c57b696815f9921f5f6c32f8fb9577986774af5a667141ea62b125454076a3489bcfb41cde7e760094', 'lara123', 5, '1', 1, 'Maipu 123', '123456789', 2, 'dD1j0uw--OleIL8p2lGGYqosUTXElD5pbm7jLFGxWS4', 1, '2025-07-13 01:55:05', 2, 1, NULL, '2', 2),
(4, 'Mora', 'Kopech', 43491828, 'morakopech@gmail.com', 'scrypt:32768:8:1$skZXySNsJhr5jHAC$bb2e25039ac655ac1ed634f698b2bdaa0b51c96559b843c57b696815f9921f5f6c32f8fb9577986774af5a667141ea62b125454076a3489bcfb41cde7e760094', 'morakopech', 5, '1', 1, 'zeballos 123', '123456789', 2, 'rCXn_mbipXl_q-7RgVjAh7qPy84Adm5ZMJXkVf3iCTI', 1, '2025-07-28 23:33:48', 2, 1, NULL, NULL, 3),
(28, 'Juan', 'Martinez', 10, 'laradelcoro01+1@gmail.com', 'scrypt:32768:8:1$kTyKA58Cb5HJc1hk$a6bb7be56bb040a3a88651e755debb9b5875d9b558747177bd1979b2814cedcb5ab4f12e70e4dee8827ee4fce63b6bf2bc8fe8a2f2da47cd3f91988d9d415ce7', 'entrenador_10', 6, '1', 1, 'N/A', '03471607768', 3, NULL, 0, NULL, 0, 0, NULL, NULL, 1),
(30, 'Alan', 'Martinez', 1857295, 'lizaotrascosas@gmail.com', 'scrypt:32768:8:1$heNa3vwZizLyCy9a$c8d522f417b2a99b8780799c39f0df96003b1a8a46e9d8e2e6f95ae0f941d0d81afcf2f8be082f28d10ca409b2b9f6a8cdea5de649ffc36608bda54206001bca', 'alan10', 3, '1', 1, 'N/A', '03471607768', 2, NULL, 0, NULL, 2, 2, NULL, NULL, 1),
(31, 'Lara', 'Admin', 999999, 'laradelcoro01+admin@gmail.com', 'scrypt:32768:8:1$KMso2fhm7yeUgRvx$cbadff5ca677227e08acf6900fc2e146e1683223b3d2acee3020cde7a83925f702e7103e9b5ec008fe95e47fc25ace165de1e473747cf707467677cf0fc94e6a', 'lara_43124684', 2, '2', 1, 'prueba', '3471607768', 1, NULL, 0, NULL, 0, 0, NULL, NULL, 1),
(32, 'Lara', 'Deportista', 55555555, 'laradelcoro01+deportista@gmail.com', 'scrypt:32768:8:1$frTvzxvpmjIgfqJ6$3766aeb21ee22476392e2da0afb79f51c3b821e14b834f57ca87e751e42ce6b378f6ca3c384018b5e606dbcafd9277f509fefc27320d6e3ce0a59d3393e0d43f', 'entrenador_55555555', 5, '2', 1, 'N/A', '03471607768', 2, NULL, 0, NULL, 2, 1, NULL, NULL, 1),
(33, 'Lara', 'Entrenador', 7777777, 'laradelcoro01+entrenador@gmail.com', 'scrypt:32768:8:1$hGsGyWQJeiTKgDXn$d6633826fb5558962bae6d6a3a927cd7f00986b84af880d6c4c68b8171574cda1ece271ac2ce3e18f0615e1646ba766e6289299667b0cdda78bcf82b09cff5f7', 'entrenador_7777777', 4, '1', 1, 'N/A', '03471607768', 3, NULL, 0, NULL, 0, 0, NULL, NULL, 3),
(36, 'Alan', 'Martinez', 101, 'laradelcoro01+33@gmail.com', 'scrypt:32768:8:1$bQILCuCPYRxNCWvj$a0f5934e33ce9df6f30e3e0b84b636bac3e86383d95f25420093e3147d19b926e9061bc75b2510db62ed1fa3bc7a1a89a42b311c84859c12f486b76169ba9849', 'entrenador_101', 5, '1', 1, 'N/A', '03471607768', 2, NULL, 0, NULL, 2, 2, NULL, NULL, 3),
(37, 'Julian', 'Carlos', 105, 'laradelcoro01+13@gmail.com', 'scrypt:32768:8:1$ghmtx6HR4ccDTbP7$39bc3d06be038c51488ca2a3ce3ad5f24501d64cd190d9f386ceff51be6c4c29133ee73c34907fefa08f7e68c13b20e2fbefeffc49c13f08496b331c53fe70ca', 'entrenador_105', 3, '1', 1, 'N/A', '03471607768', 3, NULL, 0, NULL, 0, 0, NULL, NULL, 3),
(39, 'Alan', 'Martinez', 1088, 'laradelcoro01+339@gmail.com', 'scrypt:32768:8:1$qDRTVFEVm6aYYStv$fe63ee97092023cf4df2ce9aa0bbdf48877d56b4b5a50e4c4a0750bb3a6acbecea15422c4d73e5e6d2ff8341e72ecb027ac37d43e28dc9be425e52f69ef75be7', 'entrenador_1088', 5, '1', 1, 'N/A', '03471607768', 2, NULL, 0, NULL, 2, 2, NULL, NULL, 3),
(40, 'juan', 'perez', 99999999, 'lizaotrascosas123@gmail.com', 'scrypt:32768:8:1$TK7XmuP8IzHYOAKr$81719fe43ecf200aa5178e715ecd03b1631dd04b53b76de4f84c6844ed212488e7751608750f1bc81ecf508fb8838e2f42f52acb08e11c8a95f0895818dee532', 'juan_99999999', 1, '1', 1, 'N/A', '123556', 2, NULL, 0, NULL, 2, 2, '2025-01-13 00:00:00', '3', 1),
(41, 'pepe', 'gomez', 11111111, 'lizastrappini99+depor@gmail.com', '11111111', 'pepe_11111111', 3, '1', 1, 'N/A', '123', 2, NULL, 0, NULL, 2, 2, '2025-04-10 00:00:00', '4,5', 1),
(42, 'pepe', 'luis', 0, 'voleyapp@gmail.com', 'scrypt:32768:8:1$oJ67cYsr8qg65X7a$a1c3781c8275d34107d1cb264d7d573a8934daf817fd1625a0292b395ac9e876f31db7eb863213911d0fd33818d24b59d06c7962dce53213a04e02f6f50d8d19', 'pepe_00000000', 1, '1', 1, 'N/A', '3471630099', 2, NULL, 0, NULL, 2, 2, '2025-03-13 00:00:00', '4,5', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `Calendario`
--
ALTER TABLE `Calendario`
  ADD PRIMARY KEY (`Id`);

--
-- Indices de la tabla `Contacto`
--
ALTER TABLE `Contacto`
  ADD PRIMARY KEY (`Id`);

--
-- Indices de la tabla `EstadisticaPorPartido`
--
ALTER TABLE `EstadisticaPorPartido`
  ADD PRIMARY KEY (`Id`);

--
-- Indices de la tabla `EstadisticaUsuarioPartido`
--
ALTER TABLE `EstadisticaUsuarioPartido`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `IdEstadisticaPorPartido` (`IdEstadisticaPorPartido`),
  ADD KEY `IdUsuario` (`IdUsuario`);

--
-- Indices de la tabla `Evento`
--
ALTER TABLE `Evento`
  ADD PRIMARY KEY (`Id`);

--
-- Indices de la tabla `Notificacion`
--
ALTER TABLE `Notificacion`
  ADD PRIMARY KEY (`Id`);

--
-- Indices de la tabla `Pago`
--
ALTER TABLE `Pago`
  ADD PRIMARY KEY (`Id`);

--
-- Indices de la tabla `Usuario`
--
ALTER TABLE `Usuario`
  ADD PRIMARY KEY (`Id`),
  ADD UNIQUE KEY `Id` (`Id`),
  ADD UNIQUE KEY `Dni` (`Dni`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `Calendario`
--
ALTER TABLE `Calendario`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `Contacto`
--
ALTER TABLE `Contacto`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `EstadisticaPorPartido`
--
ALTER TABLE `EstadisticaPorPartido`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `EstadisticaUsuarioPartido`
--
ALTER TABLE `EstadisticaUsuarioPartido`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `Evento`
--
ALTER TABLE `Evento`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT de la tabla `Notificacion`
--
ALTER TABLE `Notificacion`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `Pago`
--
ALTER TABLE `Pago`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `Usuario`
--
ALTER TABLE `Usuario`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
