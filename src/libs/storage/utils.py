import os
import pickle
from pathlib import Path
from typing import Any

from google.cloud import storage  # type: ignore


def upload_local_to_storage(
    local_path: Path, remote_path: str, remote_name: str
) -> None:
    client = storage.Client(os.environ["EMAP_PROJECT_ID"])
    bucket = client.get_bucket(remote_path)
    bucket.blob(remote_name).upload_from_filename(local_path)


def download_pickle_from_storage(remote_path: str, remote_name: str) -> Any:
    client = storage.Client(os.environ["EMAP_PROJECT_ID"])
    bucket = client.bucket(remote_path)
    blob = bucket.blob(remote_name)
    pickle_in = blob.download_as_string()
    return pickle.loads(pickle_in)
