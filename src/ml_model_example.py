"""
Example of FastAPI usage with API model (REST).
"""

import logging
import warnings

import arrow
import pandas as pd
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from modules.models.ml import ResponseModel
from modules.models.ml import createRequestModel
from modules.source import loadJoblibModel
from modules.source import loadJson
from src.modules.config import Configuration

load_dotenv()

warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.simplefilter(action="ignore", category=UserWarning)

logger_format = "%(asctime)s --- %(levelname)s --- %(message)s"
logger_time_format = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(
    format=logger_format,
    datefmt=logger_time_format,
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

app = FastAPI()
config = Configuration()
xgboost = loadJoblibModel(config.XGB_MODEL_URL, config.PATH_TO_XGB_MODEl)
xgb_features_sample = loadJson(config.XGB_FEATURES_SAMPLE_URL, config.PATH_TO_XGB_FEATURES_SAMPLE)

RequestModel = createRequestModel(xgb_features_sample)


@app.get(f"/health")
async def health():
    """
    Health endpoint.
    """

    return 200


@app.post(f"/api/1.0/xgb/predict", response_model=ResponseModel)
async def predictXgb(request: RequestModel):
    """
    Predict using XGBoost model.
    """

    request_members = pd.DataFrame(jsonable_encoder(request.members))

    # noinspection PyBroadException
    try:
        probabilities = xgboost.predict_proba(request_members)[:, 1]
        classification = xgboost.predict(request_members)

    except Exception:
        logger.exception("An unhandled exception occurred")
        raise HTTPException(status_code=500, detail="INTERNAL SERVER ERROR")

    else:
        response_members = pd.DataFrame()
        response_members["acceptProbability"] = probabilities
        response_members["acceptClassification"] = classification
        response_members["predictionTimestamp"] = str(arrow.get(arrow.now().date()).date())
        response_members["modelVersion"] = "1.0"
        response_members = response_members.round(decimals=3)
        return ResponseModel(members=response_members.to_dict(orient="records"))


if __name__ == "__main__":
    uvicorn.run(app, port=8020, debug=True)

"""
"""
