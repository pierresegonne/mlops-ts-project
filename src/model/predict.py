import logging

from flask import Flask, request

from src.libs.config.logger import setup_logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

setup_logging(log_level_development=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("google").setLevel(logging.INFO)


@app.route("/health")
def hello_world():
    # TODO
    return "<p>WIP</p>"


@app.route("/predict")
def predict():
    # TODO
    # Batch prediction for last data + 48h
    return "<p>WIP</p>"
