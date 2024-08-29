from datetime import datetime

from app import db


class Scam(db.Model):
    scam_id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(50), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    