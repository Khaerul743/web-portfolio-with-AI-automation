from app import db
from sqlalchemy.sql import func
from datetime import datetime

class Content(db.Model):
    __tablename__ = 'content'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body_id = db.Column(db.Integer, db.ForeignKey('body.id', ondelete='CASCADE'), nullable=False)
    subtitle = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

    body = db.relationship('Body', backref=db.backref('contents', lazy=True, cascade='all, delete-orphan'))
    def __repr__(self):
        return f"Content-Body_id {self.body_id} {self.id}"
    
    def to_dict(self):
        return {
            # "id": self.id,
            # "body_id": self.body_id,
            "subtitle": self.subtitle,
            "content": self.content,
        }