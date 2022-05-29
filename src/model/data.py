from typing import Tuple

import darts
import pandas as pd
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler

from src.dataset import get_df_from_bucket
from src.libs.config.constants import covariates_columns, ts_columns


def get_zone_data(zone_key: str) -> pd.DataFrame:
    df = get_df_from_bucket(zone_key)
    df = df.drop(columns=["zone_key"])
    # Get rid of timezone info
    df.index = df.index.tz_convert(None).to_pydatetime()
    df = df.fillna(method="ffill")
    return df


def get_timeseries(
    df: pd.DataFrame,
) -> Tuple[darts.timeseries.TimeSeries, darts.timeseries.TimeSeries]:
    ts = TimeSeries.from_dataframe(df[ts_columns])
    ts = Scaler().fit_transform(ts)  # type: ignore

    ts_covariates = TimeSeries.from_dataframe(df[covariates_columns])
    ts_covariates = Scaler().fit_transform(ts_covariates)  # type: ignore

    return ts, ts_covariates
