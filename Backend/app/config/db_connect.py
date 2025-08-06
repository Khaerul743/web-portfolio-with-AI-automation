import os
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    NAME = str(os.environ.get("DB_NAME"))
    HOST = str(os.environ.get("DB_HOST"))
    USER  = str(os.environ.get("DB_USER"))
    PASSWORD = str(os.environ.get("DB_PASSWORD"))
    PORT = str(os.environ.get("DB_PORT"))

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True