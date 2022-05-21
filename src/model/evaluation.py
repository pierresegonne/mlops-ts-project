import pickle
from pathlib import Path

from darts.metrics import mape
from darts.models.forecasting.forecasting_model import ForecastingModel

from src.libs.config.constants import Zone
from src.model.data import get_timeseries, get_zone_data


def get_model(name: str, tmp: bool = True) -> ForecastingModel:
    if tmp:
        path = path = Path(__file__).parent.resolve() / f"_tmp/{name}.pkl"
        # pickle model
        with open(path, "rb") as f:
            model = pickle.load(f)
    else:
        raise NotImplementedError
    return model


def save_eval(eval: object, name: str, tmp: bool = True) -> None:
    if tmp:
        path = path = Path(__file__).parent.resolve() / f"_tmp/{name}.pkl"
        # pickle model
        with open(path, "wb") as f:
            pickle.dump(eval, f)
    else:
        raise NotImplementedError


def run():
    for zone_key in Zone:
        df = get_zone_data(zone_key)
        ts, covariates = get_timeseries(df)
        train, test = ts.split_before(0.75)
        model = get_model(zone_key)
        forecast = model.predict(len(test), future_covariates=covariates)
        eval = mape(test.univariate_component("power_production_wind_avg"), forecast)
        save_eval(eval, zone_key + "_eval")


if __name__ == "__main__":
    run()
