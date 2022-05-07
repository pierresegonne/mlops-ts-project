# syntax=docker/dockerfile:1
FROM python:3.8.12
ENV APP_HOME /app
WORKDIR $APP_HOME
# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV FLASK_APP=src/__main__.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
COPY .python-version .python-version
RUN apt-get update
RUN apt-get install gcc -y
RUN python -m pip install --upgrade pip
RUN pip install poetry==1.1.12
RUN poetry config virtualenvs.create false
RUN poetry install
EXPOSE 5000
COPY src src
# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 src.__main__:app