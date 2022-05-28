import logging

from flask import Flask, request

from src.libs.config.logger import setup_logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

from src.dataset import update as update_dataset

setup_logging(log_level_development=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("google").setLevel(logging.INFO)


@app.route("/")
def hello_world():
    return "<p>Welcome to the TS project!</p>"


@app.route("/update_data")
def update_data():
    logger.info("Update data: starting")
    update_dataset()
    logger.info("Update data: done")
    return "<p>Updated data to bucket!</p>"


@app.route("/update_model")
def update_model():
    # TODO
    # Could do: create training image, upload to registry and make call to vertexAI to start the training.
    # If in prod, then don't need to trigger a build of the training image
    # This assumes that the training image is already built and available in the registry
    # E.g that there is CD
    # This is actually the last thing we should worry about
    pass
