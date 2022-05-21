import logging
import os
from io import StringIO

import arrow
import pandas as pd
from google.cloud import storage  # type: ignore[attr-defined]
from numpy import nan

logger = logging.getLogger(__name__)

from src.libs.config.constants import DATA_START_DATE, Zone
from src.libs.db.flowtraced_data import query_flowtraced_data

BUCKET_NAME = "mlops-ts-project"
BUCKET_DATA_PATH = "data"

relevant_columns = [
    "zone_key",
    "power_production_wind_avg",
    "power_production_solar_avg",
    "latest_forecasted_solar_avg",
    "latest_forecasted_wind_x_avg",
    "latest_forecasted_wind_y_avg",
    "latest_forecasted_dewpoint_avg",
    "latest_forecasted_temperature_avg",
    "latest_forecasted_precipitation_avg",
    "latest_forecasted_production_wind_avg",
    "latest_forecasted_production_solar_avg",
]


def get_df_from_bucket(name: str) -> pd.DataFrame:
    client = storage.Client(os.environ["EMAP_PROJECT_ID"])

    bucket = client.get_bucket(BUCKET_NAME)
    data_str = bucket.blob(f"{BUCKET_DATA_PATH}/{name}.csv").download_as_text()
    df = pd.read_csv(StringIO(data_str), index_col="datetime", parse_dates=True)
    df = df.fillna(nan)
    df = df.astype({c: float for c in set(relevant_columns) - {"zone_key"}})
    return df


def save_df_to_bucket(name: str, df: pd.DataFrame) -> None:
    client = storage.Client(os.environ["EMAP_PROJECT_ID"])

    bucket = client.get_bucket(BUCKET_NAME)
    bucket.blob(f"{BUCKET_DATA_PATH}/{name}.csv").upload_from_string(
        df.to_csv(), "text/csv"
    )


def _clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """Only keep relevant columns for the model"""
    # datetime is the index
    # NaNs replaced by empty strings
    df = df[relevant_columns].copy()
    df = df.fillna(method="ffill")
    return df


def update() -> None:
    time_range = (DATA_START_DATE, arrow.now().format("YYYY-MM-DD"))

    for zone in Zone:
        logger.info(f"Updating {zone} between {time_range}")
        df = _clean_df(query_flowtraced_data(zone, time_range))
        save_df_to_bucket(zone.value, df)
