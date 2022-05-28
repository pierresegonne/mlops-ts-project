import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.libs.config.constants import Zone
from src.model.data import get_zone_data

""" Script to analyse the data to include in the blog post """


def _fetch_all_data() -> pd.DataFrame:
    _dfs = []
    for zone_key in Zone:
        _df = get_zone_data(zone_key)
        _df.loc[:, "zone_key"] = zone_key.value
        _dfs.append(_df)
    return pd.concat(_dfs)


def _plot_pairplot(df: pd.DataFrame) -> None:
    breakpoint()
    g = sns.pairplot(df, hue="zone_key")


def _plot_timeseries(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(12, 8))
    for zone_key in Zone:
        df_zone = df[df["zone_key"] == zone_key]
        df_zone.loc[:, "power_production_wind_avg"].plot(ax=ax, label=zone_key)
    ax.set_xlabel("Date")
    ax.set_ylabel("Wind power production [MW]")
    ax.legend()


def plot_data() -> None:
    """Plot the data"""
    df = _fetch_all_data()
    # Pairplot
    _plot_pairplot(df)
    # Timeseries
    _plot_timeseries(df)
    plt.show()


if __name__ == "__main__":
    plot_data()
