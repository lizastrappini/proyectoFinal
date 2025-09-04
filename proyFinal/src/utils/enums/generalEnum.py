import enum

class RolEnum(enum.IntEnum): 
    Admin = 1
    Deportista = 2
    Entrenador = 3


class EstadoEnum(enum.IntEnum): 
    Activo = 1
    Inactivo = 2

class EstadoPagoEnum(enum.IntEnum):
    Pago = 1
    NoPago = 2
    Pendiente = 3
    
class LocalidadEnum(enum.IntEnum): 
    Rosario = 1
    Funes = 2
    VillaConstitucion = 3
    SanLorenzo = 5
    Casilda = 6
    PuebloEsher = 7
    Roldan = 8
    Zavalla = 9
    Perez = 4
    ArroyoSeco = 10
    VillaGobernadorGalvez = 11
    Carcaraña = 12
    CañadaDeGomez = 13
    SanNicolas = 14 
    NoDefinido = 0


class CategoriaEnum(enum.IntEnum): 
    Sub12 = 1
    Sub13 = 2
    Sub14 = 3
    Sub16 = 4
    Sub18 = 5
    Sub21 = 6
    Primera = 7
    NoEspecificada = 0
    
class DivisionEnum(enum.IntEnum):
    A = 1
    B = 2
    
class RamaEnum(enum.IntEnum):
    Femenino = 1
    Masculino= 2


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
    
class FederadoEnum(enum.IntEnum):
    Federado = 1
    NoFederado = 2
    NoAplica = 3


class ContrincantesEnum(enum.IntEnum):
    Sonder = 1
    Central = 2
    Nautico = 3
    Normal3 = 4
    ElTala = 5
    Citta = 6
    Ger = 7
    Provincial = 8
    RedEstar = 9
    Rowing = 10
    Atalaya  = 11
    Regatas =12
    Libertad = 13
    Newells = 14
    Estudiantil = 15
    Sportsmen = 17
    Bancario = 18
    Fisherton = 19


class ResultadoEnum(enum.IntEnum):
    G = 1
    P = 2
    