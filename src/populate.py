"""
Populate DB.
"""

import os

from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

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
    Base.metadata.create_all(sql_engine)
    for index in range(10):
        member = MemberORM(id=index, name=fake.first_name(), position=fake.job())
        session.add(member)
        session.commit()
