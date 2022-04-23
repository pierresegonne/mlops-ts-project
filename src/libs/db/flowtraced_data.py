from typing import Tuple

import arrow
import pandas as pd

from libs.db.connection import get_pg_connection


def query_flowtraced_data(zone_key: str, time_range: Tuple[str, str]) -> pd.DataFrame:
    connection = get_pg_connection()

    query = """
    SELECT
        *
    FROM
        flowtraced_data
    WHERE 1=1
        AND zone_key = %(zone_key)s
        AND datetime >= %(start)s
        AND datetime <= %(end)s
    ORDER BY datetime ASC;
    """

    start_datetime, end_datetime = time_range
    params = {
        "zone_key": zone_key,
        "start": arrow.get(start_datetime).format(),
        "end": arrow.get(end_datetime).format(),
    }

    df = pd.read_sql_query(
        query,
        connection,
        params=params,
        index_col=["datetime"],
        parse_dates=["datetime"],
    )

    # split out data json into columns
    # NOTE other nested columns are not expanded (e.g capacity)
    # but we might want to feed them to compute_features in the future
    if not df.empty:
        df = pd.merge(
            df,
            # This creates a series where columns are the keys of data blob
            df.data.apply(pd.Series),  # pylint: disable=no-member
            left_index=True,
            right_index=True,
            suffixes=(None, "_data"),
        )
        if "origin_data" in df.columns:
            # Handle column duplicate from merge
            assert df.origin.equals(df.origin_data)
            df = df.drop(columns=["origin_data"])
    df = df.drop(columns=["data"])
    return df
