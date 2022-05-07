import os


def serve_dev():
    os.system(
        "FLASK_APP=src.__main__:app FLASK_ENV=development poetry run flask run --port=8080"
    )
