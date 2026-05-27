from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


database_url = "sqlite:///./db.sqlite"
engine = create_engine(database_url)

session_generator = sessionmaker(
    engine,
)
