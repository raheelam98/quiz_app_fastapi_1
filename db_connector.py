from sqlmodel import Session, create_engine, SQLModel
from quiz_backend.setting import db_url  #, test_db_url

# adjust connection string for PostgreSQL with psycopg2 driver
connection_string = str(db_url).replace("postgresql", "postgresql+psycopg2")

# create the SQLAlchemy engine
engine = create_engine(connection_string, echo=True)

# function to create database and tables based on SQLModel metadata
def createTable():
    SQLModel.metadata.create_all(engine)

# function to get a session for database operations
def get_session():
    # using context manager to manage the database session
    with Session(engine) as session:
        yield session   
