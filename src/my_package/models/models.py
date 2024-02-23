from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ML_Models(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_path = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"{self.model_path}"