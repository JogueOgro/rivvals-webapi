from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
db_path = os.getenv('DB_PATH')

engine = create_engine(db_path)
Session = sessionmaker(bind=engine)