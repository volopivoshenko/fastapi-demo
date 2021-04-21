"""
ORM and Query models for GraphQL example.
"""

from typing import Any

import graphene
from graphene_pydantic import PydanticObjectType
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MemberORM(Base):
    """
    ORM of a member
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

        return MemberGQL()
