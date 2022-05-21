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
