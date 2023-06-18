"""A sqlalchemy.orm Session."""
from dnd.core import uncached_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(uncached_settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
