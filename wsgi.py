from app.app import create_app
from flask_migrate import Migrate
from app.db.db import db
import os


credentials_path = "./credentials.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

app = create_app("production")
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()
