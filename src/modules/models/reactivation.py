"""
SQL ORM, pydantic model, GraphQL model for GraphQL example.
"""

from graphene_pydantic import PydanticObjectType
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ReactivationPredictionORM(Base):
    """
    ORM of the ML model output.
    """

    __tablename__ = "reactivation_prediction"

    index = Column(Integer, primary_key=True)
    prediction_date = Column(Date)
    member_id = Column(Integer)
    product = Column(String)
    lapsed_days = Column(Integer)
    reactivation_probability = Column(Float)
    reactivation_classification = Column(Integer)
    model_version = Column(String)


ReactivationPredictionPydantic = sqlalchemy_to_pydantic(ReactivationPredictionORM)


class ReactivationPredictionGraphQL(PydanticObjectType):
    """
    GraphQL model of the ML model output.
    """

    class Meta:
        model = ReactivationPredictionPydantic
