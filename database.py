import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Helper function to configure database
def configure_db(app):
    # Configure the database, use PostgreSQL if available, or fallback to SQLite
    database_url = os.environ.get("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        # Heroku-style PostgreSQL URL needs to be updated for SQLAlchemy 1.4+
        database_url = database_url.replace("postgres://", "postgresql://")
        
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url or "sqlite:///sqliscanner.db"
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize the app with the extension
    db.init_app(app)