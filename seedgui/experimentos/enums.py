from enum import Enum

class TimeInterval(Enum):
    ten_seconds = '10 secs'
    fifteen_mins = '15 mins'
    thirty_mins = '30 mins'
    one_hour = '1 hour'
    two_hours = '2 hour'
    three_hours = '3 hour'

class SetupStatus(Enum):
    activo = 'Active'
    creado = 'Created'
    finalizado = 'Finished'