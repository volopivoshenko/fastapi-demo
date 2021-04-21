"""
Example of GraphQL usage with FastAPI.
"""

import os
from typing import Any

import graphene
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from graphene_pydantic import PydanticObjectType
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.graphql import GraphQLApp

load_dotenv()

app = FastAPI()
sql_engine = create_engine(os.getenv("DB_CONNECTION_STRING"))
Base = declarative_base()


class MemberORM(Base):
    """
    SQL ORM of a member
    """

    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    position = Column(String)


# Pydantic model of the member
MemberPydantic = sqlalchemy_to_pydantic(MemberORM)


class MemberGQL(PydanticObjectType):
    """
    GraphQL model of a member.
    """

    class Meta:
        model = MemberPydantic


class QueryGQL(graphene.ObjectType):
    """
    GraphQL query.
    """

    member = graphene.Field(MemberGQL, id=graphene.Int(required=True))

    @staticmethod
    def resolve_member(root: Any, info: Any, id: int) -> MemberGQL:
        """
        Response on "member" query.
        """

        _ = root
        _ = info

        session = sessionmaker(sql_engine)()
        Base.metadata.create_all(sql_engine)

        response, *_ = session.query(MemberORM).filter(MemberORM.id == id)
        response = {
            column.name: getattr(response, column.name) for column in MemberORM.__table__.columns
        }

        # noinspection PyArgumentList
        return MemberGQL(**response)


# noinspection PyTypeChecker
app.add_route("/", GraphQLApp(schema=graphene.Schema(query=QueryGQL)))

if __name__ == "__main__":
    uvicorn.run(app, port=8000, debug=True)
