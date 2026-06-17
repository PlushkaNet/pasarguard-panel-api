from enum import StrEnum

class Status(StrEnum):
    ACTIVE   = "active"
    DISABLED = "disabled"
    LIMITED  = "limited"
    EXPIRED  = "expired"
    ON_HOLD  = "on_hold"