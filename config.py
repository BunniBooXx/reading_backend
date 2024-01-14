import os 

class Config:
    FLASK_APP= os.environ.get("FLASK_APP")
    FLASK_DEBUG= os.environ.get("FLASK_DEBUG")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    # "postgres://reading_backend_user:WYJ2Tx2B6rtwqbfEYQOYKXxOrhnUIvcG@dpg-cmhikj6n7f5s739t5rjg-a.oregon-postgres.render.com/readingbackend"
    
    SQLALCHEMY_TRACK_MODIFICATIONS= False

    SECRET_KEY = os.environ.get("SECRET_KEY")