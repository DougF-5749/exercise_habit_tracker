from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# Load environment variable for URL to fatabase
load_dotenv()
URL_TO_DATABASE = os.getenv("URL_TO_DATABASE")

# Set up database engine, session, and base
engine = create_engine(URL_TO_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()