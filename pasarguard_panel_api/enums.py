""" File with code for enums for convenience """
from enum import StrEnum

class Status(StrEnum):
    """ Statuses for user in Pasarguard panel """
    ACTIVE   = "active"
    DISABLED = "disabled"
    LIMITED  = "limited"
    EXPIRED  = "expired"
    ON_HOLD  = "on_hold"
