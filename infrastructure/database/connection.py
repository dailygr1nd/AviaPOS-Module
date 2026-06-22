from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql+psycopg://aviapos:aviapos@localhost:5432/aviapos"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True
)