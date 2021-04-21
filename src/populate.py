"""
Populate DB.
"""

import logging
import os

from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

logger = logging.getLogger(__name__)
sql_engine = create_engine(os.getenv("DB_CONNECTION_STRING"))
session = sessionmaker(sql_engine)()
fake = Faker()
Base = declarative_base()


class MemberORM(Base):
    """
    SQL ORM of a member
    """

    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    position = Column(String)


if __name__ == "__main__":
    metadata = MetaData(sql_engine)
    table = metadata.tables.get("members")
    if table is not None:
        MemberORM.__table__.drop(sql_engine)

    Base.metadata.create_all(sql_engine)
    for index in range(100):
        member = MemberORM(id=index, name=fake.first_name(), position=fake.job())
        session.add(member)
        session.commit()
