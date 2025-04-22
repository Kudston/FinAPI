from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from typing import Iterator
from src.config import Settings

class DatabaseConfig:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_db_config()
        return cls._instance
    
    def _init_db_config(self):
        self.app_settings = Settings()
        
        # Create engine with optimized connection pooling
        self.engine = create_engine(
            self.app_settings.get_full_db_url(),
            poolclass=QueuePool,
            pool_size=5,  
            max_overflow=10, 
            pool_timeout=30, 
            pool_recycle=1800,
            pool_pre_ping=True,
            echo=False
        )
        
        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.engine
        )

# Create an instance of database configuration
db_config = DatabaseConfig()

Base = declarative_base()

#get database session
def get_db() -> Iterator[Session]:
    db = db_config.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Optional: Connection management functions
def get_engine():
    """
    Returns an engine with connection pooling.
    """
    return db_config.engine

def close_db_connections():
    """
    Dispose of all connections in the pool.
    """
    if hasattr(db_config, 'engine'):
        db_config.engine.dispose()