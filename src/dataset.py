import logging

import arrow
import pandas as pd
from google.cloud import storage

storage_client = storage.Client()

logger = logging.getLogger(__name__)

from src.libs.config.constants import DATA_START_DATE, Zone
from src.libs.db.flowtraced_data import query_flowtraced_data

BUCKET_NAME = "mlops-ts-project"
BUCKET_DATA_PATH = "data"


def save_df_to_bucket(name: str, df: pd.DataFrame) -> None:
    client = storage.Client()

    bucket = client.get_bucket(BUCKET_NAME)
    bucket.blob(f"{BUCKET_DATA_PATH}/{name}.csv").upload_from_string(
        df.to_csv(), "text/csv"
    )


def update() -> None:
    time_range = (DATA_START_DATE, arrow.now().format("YYYY-MM-DD"))

    for zone in Zone:
        logger.info(f"Updating {zone} between {time_range}")
        df = query_flowtraced_data(zone, time_range)
        save_df_to_bucket(zone.value, df)
