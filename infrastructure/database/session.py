from sqlalchemy.orm import sessionmaker

from infrastructure.database.connection import (
    engine
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)