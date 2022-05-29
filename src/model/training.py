import logging
import os
import pickle
from pathlib import Path

from darts.models import AutoARIMA
from darts.models.forecasting.forecasting_model import ForecastingModel

from src.libs.config.constants import Zone
from src.libs.storage.utils import upload_local_to_storage
from src.model.data import get_timeseries, get_zone_data
from src.model.evaluation import run as run_evaluation

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_model() -> ForecastingModel:
    return AutoARIMA()  # type: ignore


def save_model(model: ForecastingModel, name: str) -> None:
    logger.info(f"Saving model for zone: {name}")
    base_path = Path(__file__).parent.resolve()
    if not os.path.exists(base_path / "_tmp"):
        os.makedirs(base_path / "_tmp")
    local_path = base_path / f"_tmp/{name}.pkl"
    # pickle model
    with open(local_path, "wb") as f:
        pickle.dump(model, f)
    remote_artifact_storage = os.environ["AIP_MODEL_DIR"]
    if remote_artifact_storage:
        upload_local_to_storage(local_path, remote_artifact_storage, name)
    logger.info(
        f"Finished saving model for zone: {name} locally at {local_path} | remote at {remote_artifact_storage}"
    )

    """

    AIP_MODEL_DIR: a Cloud Storage URI of a directory intended for saving model artifacts.
    AIP_CHECKPOINT_DIR: a Cloud Storage URI of a directory intended for saving checkpoints.
    AIP_TENSORBOARD_LOG_DIR: a Cloud Storage URI of a directory intended for saving TensorBoard logs. See Using Vertex AI TensorBoard with custom training.

    """


def run() -> None:
    for zone_key in Zone:
        logger.info(f"Fetching data for zone: {zone_key}")
        df = get_zone_data(zone_key)
        logger.info(f"Finished fetching data for zone: {zone_key}. Shape: {df.shape}")
        ts, covariates = get_timeseries(df)
        train, _ = ts.split_before(0.75)
        model = get_model()
        logger.info(f"Training model for zone: {zone_key}")
        model.fit(
            train.univariate_component("power_production_wind_avg"),
            future_covariates=covariates,
        )  # type: ignore
        logger.info(f"Finished training model for zone: {zone_key}")
        save_model(model, zone_key)
    run_evaluation()


if __name__ == "__main__":
    run()
