import pickle
from pathlib import Path

from darts.models import AutoARIMA
from darts.models.forecasting.forecasting_model import ForecastingModel

from src.libs.config.constants import Zone
from src.model.data import get_timeseries, get_zone_data
from src.model.evaluation import run as run_evaluation


def get_model() -> ForecastingModel:
    return AutoARIMA() # type: ignore


def save_model(model: ForecastingModel, name: str, tmp: bool = True) -> None:
    if tmp:
        path = Path(__file__).parent.resolve() / f"_tmp/{name}.pkl"
        # pickle model
        with open(path, "wb") as f:
            pickle.dump(model, f)
    else:
        raise NotImplementedError


def run() -> None:
    for zone_key in Zone:
        df = get_zone_data(zone_key)
        ts, covariates = get_timeseries(df)
        train, test = ts.split_before(0.75)
        model = get_model()
        model.fit(
            train.univariate_component("power_production_wind_avg"),
            future_covariates=covariates,
        ) # type: ignore
        save_model(model, zone_key)
    run_evaluation()


if __name__ == "__main__":
    run()
