"""
Populate DB.
"""

import logging
import os

from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from modules.models.reactivation import ReactivationPredictionORM

load_dotenv()

logger = logging.getLogger(__name__)
sql_engine = create_engine(os.getenv("DB_CONNECTION_STRING"))
session = sessionmaker(sql_engine)()
fake = Faker()
Base = declarative_base()


if __name__ == "__main__":
    # drop table if it exists
    metadata = MetaData(sql_engine)
    table = metadata.tables.get("reactivation_prediction")
    ReactivationPredictionORM.__table__.drop(sql_engine)
    ReactivationPredictionORM.__table__.create(sql_engine)

    Base.metadata.create_all(sql_engine)

    for index in range(100):
        row = ReactivationPredictionORM(
            index=index,
            prediction_date=fake.date(),
            member_id=fake.pyint(),
            product=fake.company(),
            lapsed_days=fake.pyint(10, 60),
            reactivation_probability=fake.pyfloat(min_value=0, max_value=1, right_digits=3),
            reactivation_classification=fake.pyint(0, 1),
            model_version="1.0",
        )
        session.add(row)
        session.commit()
