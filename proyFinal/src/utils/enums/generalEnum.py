import enum

class RolEnum(enum.IntEnum): 
    Admin = 1
    Deportista = 2
    SubComision = 3
    Entrenador = 4


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