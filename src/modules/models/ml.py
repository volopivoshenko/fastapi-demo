"""
Models for ML model example.
"""

from typing import Dict
from typing import List
from typing import Union

import pydantic
from pydantic import BaseModel
from pydantic import Field
from typing_extensions import TypedDict


def createRequestModel(features_sample: Dict[str, Union[int, float, str]]) -> BaseModel:
    """
    Create request model based on features.
    """

    # noinspection PyTypedDict
    member = TypedDict(
        "MemberRequestModel", {feature: type(value) for feature, value in features_sample.items()}
    )
    # noinspection PyUnresolvedReferences
    MemberRequestModel = pydantic.create_model_from_typeddict(member)

    class RequestModel(BaseModel):
        """
        Request model.
        """

        members: List[MemberRequestModel] = Field(..., min_items=1)

    # noinspection PyTypeChecker
    return RequestModel


class MemberResponseModel(BaseModel):
    """
    Response model.
    """

    prediction_timestamp: str = Field(None, alias="predictionTimestamp")
    model_version: str = Field(None, alias="modelVersion")
    accept_probability: float = Field(None, alias="acceptProbability")
    accept_classification: float = Field(None, alias="acceptClassification")


class ResponseModel(BaseModel):
    """
    Response models.
    """

    members: List[MemberResponseModel]
