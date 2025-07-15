import enum

class RolEnum(enum.IntEnum): 
    Admin = 1
    Deportista = 2
    Entrenador = 3


class EstadoEnum(enum.IntEnum): 
    Activo = 1
    Inactivo = 2


class LocalidadEnum(enum.IntEnum): 
    Rosario = 1


class EstadoPagoEnum(enum.IntEnum):
    Pago = 1
    NoPago = 2

class CategoriaEnum(enum.IntEnum): 
    Sub12 = 1
    Sub13 = 2
    Sub14 = 3
    Sub16 = 4
    Sub18 = 5
    Sub21 = 6
    Primera = 7


def obtenerNombreRol(valor_int):
    try:
        return RolEnum(valor_int).name
    except ValueError:
        return None 
    

class TipoEventoEnum(enum.IntEnum):
    Entrenamiento = 1
    Partido = 2
    Vacaciones = 3
    SuspensionEntrenamiento = 4
    Torneo = 5
    Recaudacion = 6
