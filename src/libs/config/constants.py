from enum import Enum

DATA_START_DATE = "2021-01-01"


class Zone(str, Enum):
    DK_DK1 = "DK-DK1"
    ES = "ES"
    US_CENT_SWPP = "US-CENT-SWPP"


ts_columns = ["power_production_wind_avg", "power_production_solar_avg"]
covariates_columns = [
    "latest_forecasted_production_wind_avg",
    "latest_forecasted_production_solar_avg",
    "latest_forecasted_solar_avg",
    "latest_forecasted_wind_x_avg",
    "latest_forecasted_wind_y_avg",
    "latest_forecasted_dewpoint_avg",
    "latest_forecasted_temperature_avg",
    "latest_forecasted_precipitation_avg",
]
