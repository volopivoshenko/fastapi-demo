"""
Example of GraphQL usage with FastAPI.
"""

import os
from typing import Any
from typing import List

import graphene
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.graphql import GraphQLApp

from modules.models.reactivation import ReactivationPredictionGraphQL
from modules.models.reactivation import ReactivationPredictionORM

load_dotenv()

app = FastAPI()
sql_engine = create_engine(os.getenv("DB_CONNECTION_STRING"))
session = sessionmaker(sql_engine)()
Base = declarative_base()
Base.metadata.create_all(sql_engine)


class QueryGraphQL(graphene.ObjectType):
    """
    GraphQL query.

    Notes
    -----
    hlr_members - members who are likely to reactivate.
    """

    member = graphene.Field(ReactivationPredictionGraphQL, member_id=graphene.Int(required=True))
    hlr_members = graphene.List(ReactivationPredictionGraphQL)

    @staticmethod
    def resolve_member(root: Any, info: Any, member_id: int) -> ReactivationPredictionGraphQL:
        """
        Response on "member" query.
        """

        _ = root
        _ = info

        response, *_ = session.query(ReactivationPredictionORM).filter(
            ReactivationPredictionORM.member_id == member_id
        )
        response = {
            column.name: getattr(response, column.name)
            for column in ReactivationPredictionORM.__table__.columns
        }

        # noinspection PyArgumentList
        return ReactivationPredictionGraphQL(**response)

    @staticmethod
    def resolve_hlr_members(root: Any, info: Any) -> List[ReactivationPredictionGraphQL]:
        """
        Response on "hlr_members" query.
        """

        _ = root
        _ = info

        response = session.query(ReactivationPredictionORM).filter(
            ReactivationPredictionORM.reactivation_classification == 1
        )
        responses = [
            {
                column.name: getattr(record, column.name)
                for column in ReactivationPredictionORM.__table__.columns
            }
            for record in response
        ]

        # noinspection PyArgumentList
        return [ReactivationPredictionGraphQL(**record) for record in responses]


# noinspection PyTypeChecker
app.add_route("/", GraphQLApp(schema=graphene.Schema(query=QueryGraphQL)))

if __name__ == "__main__":
    uvicorn.run(app, port=8030, debug=True)
