from os import environ

from sqlalchemy import create_engine
from sqlalchemy import engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = engine.URL.create(
    'mysql+mysqlconnector',
    username='root',
    password=environ.get('MYSQL_ROOT_PWD'),
    host=environ.get('MYSQL_HOST'),
    port=environ.get('MYSQL_TCP_PORT_EXAMPLES'),
    database=environ.get('MYSQL_DB_NAME'),
)
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
