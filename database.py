from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://20241204-fastapi:123456@localhost/20241204-fastapi"

# Création de l'engine SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour nos modèles
Base = declarative_base()
