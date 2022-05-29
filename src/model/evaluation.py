import logging
import os
import pickle
from pathlib import Path
from typing import cast

from darts.metrics import mape
from darts.models.forecasting.forecasting_model import ForecastingModel

from src.libs.config.constants import Zone
from src.libs.storage.utils import download_pickle_from_storage, upload_local_to_storage
from src.model.data import get_timeseries, get_zone_data

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_model(name: str, tmp: bool = True) -> ForecastingModel:
    logger.info(f"Fetching model for zone: {name}")
    local_path = Path(__file__).parent.resolve() / f"_tmp/{name}.pkl"
    remote_artifact_storage = os.environ["AIP_MODEL_DIR"]
    if local_path.exists():
        # pickle model
        with open(local_path, "rb") as f:
            model = pickle.load(f)
        path = str(local_path)
    elif remote_artifact_storage:
        model = download_pickle_from_storage(remote_artifact_storage, name)
        path = remote_artifact_storage
    else:
        raise FileNotFoundError(f"No model found for zone: {name}")
    logger.info(f"Finished fetching model for zone: {name}, path: {path}")
    return cast(ForecastingModel, model)


def save_eval(eval: object, name: str, tmp: bool = True) -> None:
    logger.info(f"Saving model for zone: {name}")
    base_path = Path(__file__).parent.resolve()
    if not os.path.exists(base_path / "_tmp"):
        os.makedirs(base_path / "_tmp")
    local_path = base_path / f"_tmp/{name}.pkl"
    # pickle model
    with open(local_path, "wb") as f:
        pickle.dump(eval, f)
    remote_artifact_storage = os.environ["AIP_MODEL_DIR"]
    if remote_artifact_storage:
        upload_local_to_storage(local_path, remote_artifact_storage, name)
    logger.info(
        f"Finished saving evaluation for zone: {name} locally at {local_path} | remote at {remote_artifact_storage}"
    )


def run() -> None:
    for zone_key in Zone:
        logger.info(f"Fetching data for zone: {zone_key}")
        df = get_zone_data(zone_key)
        logger.info(f"Finished fetching data for zone: {zone_key}. Shape: {df.shape}")
        ts, covariates = get_timeseries(df)
        train, test = ts.split_before(0.75)
        model = get_model(zone_key)
        logger.info(f"Evaluating model for zone: {zone_key}")
        forecast = model.predict(len(test), future_covariates=covariates)  # type: ignore
        eval = mape(test.univariate_component("power_production_wind_avg"), forecast)
        logger.info(f"Finished evaluating model for zone: {zone_key}")
        save_eval(eval, zone_key + "_eval")


if __name__ == "__main__":
    run()
