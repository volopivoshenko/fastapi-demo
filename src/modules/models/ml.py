"""
Models for ML model example.
"""

import logging
from typing import Dict
from typing import List
from typing import Union

import pydantic
from pydantic import BaseModel
from pydantic import conlist
from pydantic import Field
from pydantic import validator
from typing_extensions import TypedDict

logger = logging.getLogger(__name__)


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

        # @validator("members")
        # def nonEmptyList(cls, value: List[MemberRequestModel]) -> List[MemberRequestModel]:
        #     """
        #     Check if input list with members features are not empty
        #     """
        #
        #     if value:
        #         return value
        #
        #     else:
        #         msg = "Empty request"
        #         logger.exception(msg)
        #         raise ValueError(msg)

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
