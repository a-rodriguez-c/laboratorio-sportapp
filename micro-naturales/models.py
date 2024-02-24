from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Event('{self.name}', '{self.location}', '{self.severity}')"