"""
Load artefacts.
"""

import json
import logging
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Union

import xgboost
from artifactory import ArtifactoryPath
from joblib import load

logger = logging.getLogger(__name__)


def downloadArtifact(url: str, path: str) -> bool:
    """
    Download artifact.
    """

    logger.info("Downloading.")

    repository = ArtifactoryPath(url)

    with repository.open() as fd:
        with open(path, "wb") as out:
            out.write(fd.read())

    logger.info("Downloaded.")
    return True


def loadJoblibModel(url: str, path: str) -> Union[xgboost.XGBClassifier, Any]:
    """
    Load Joblib models.
    """

    _ = url
    path = Path(path)
    logger.info(f"Loading {path.name}.")

    # downloadArtifact(url, path)
    model = load(path)

    logger.info("Loaded.")
    return model


def loadJson(url: str, path: str) -> Dict[str, Union[int, float, str]]:
    """
    Load jsons.
    """

    _ = url
    path = Path(path)
    logger.info(f"Loading {path.name}.")

    # downloadArtifact(url, path)
    with open(path, "r") as file:
        structure = json.loads(file.read())
        file.close()

    logger.info("Loaded.")
    return structure
