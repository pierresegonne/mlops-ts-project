from enum import Enum

DATA_START_DATE = "2021-01-01"


class Zone(str, Enum):
    DK_DK1 = "DK-DK1"
    ES = "ES"
    US_CENT_SWPP = "US-CENT-SWPP"
