"""
Example of GraphQL usage with FastAPI.
"""

from typing import Any

import graphene
import uvicorn
from fastapi import FastAPI
from starlette.graphql import GraphQLApp

MEMBERS = {
    0: {"name": "Volo", "position": "ML Engineer"},
    1: {"name": "Diane.", "position": "Planner"},
}


class Member(graphene.ObjectType):
    """
    Member object.
    """

    id = graphene.Int()
    name = graphene.String()
    position = graphene.String()


class Query(graphene.ObjectType):
    """
    GraphQL query.
    """

    member = graphene.Field(Member, id=graphene.Int(required=True))

    @staticmethod
    def resolve_member(root: Any, info: Any, id: int) -> Member:
        """
        Response on "me" query.
        """

        _ = root
        _ = info

        return Member(id=id, **MEMBERS.get(id, {"name": "undefined", "position": "undefined"}))


app = FastAPI()
# noinspection PyTypeChecker
app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))

if __name__ == "__main__":
    uvicorn.run(app, port=8000, debug=True)
