import logging

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.libs.config.constants import Zone
from src.model.data import get_zone_data

""" Script to analyse the data to include in the blog post """

# Setup debug level debugger
logger = logging.getLogger(__name__)


def _fetch_all_data() -> pd.DataFrame:
    _dfs = []
    logger.debug("[FETCH] - start fetching data for all zones")
    for zone_key in Zone:
        _df = get_zone_data(zone_key)
        _df.loc[:, "zone_key"] = zone_key.value
        _dfs.append(_df)
    df = pd.concat(_dfs)
    logger.debug(
        "[FETCH] - done fetching data for all zones. Shape: {}".format(df.shape)
    )
    return df


def _filter_columns(df: pd.DataFrame) -> pd.DataFrame:
    columns_to_keep_for_visualisation = [
        "zone_key",
        "power_production_wind_avg",
        "latest_forecasted_production_wind_avg",
        "latest_forecasted_wind_x_avg",
        "latest_forecasted_wind_y_avg",
        "latest_forecasted_temperature_avg",
    ]
    return df.loc[:, columns_to_keep_for_visualisation]


def _plot_pairplot(df: pd.DataFrame) -> None:
    logger.debug("[PLOT] - start plotting pairplot")
    g = sns.pairplot(df.reset_index(), hue="zone_key")


def _plot_timeseries(df: pd.DataFrame) -> None:
    logger.debug("[PLOT] - start plotting timeseries")
    fig, ax = plt.subplots(figsize=(12, 8))
    for zone_key in Zone:
        df_zone = df[df["zone_key"] == zone_key]
        df_zone.loc[:, "power_production_wind_avg"].plot(ax=ax, label=zone_key.value)
    ax.set_xlabel("Date")
    ax.set_ylabel("Wind power production [MW]")
    ax.legend()


def plot_data() -> None:
    """Plot the data"""
    df = _fetch_all_data()
    # Subsample to make it easier to plot
    df = df.iloc[::10]
    df = _filter_columns(df)
    # Pairplot
    _plot_pairplot(df)
    # Timeseries
    _plot_timeseries(df)
    plt.show()


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    plot_data()
