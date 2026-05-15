from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://platform:platform123@100.30.199.241:30432/platformdb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()