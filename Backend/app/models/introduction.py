from app import db
from sqlalchemy.sql import func
from datetime import datetime

class Introduction(db.Model):
    __tablename__ = 'introduction'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id', ondelete='CASCADE'), nullable=False, unique=True)
    hook = db.Column(db.String(255), nullable=False)
    purpose = db.Column(db.String(255), nullable=False)

    # hubungan balik ke blog (One-to-One)
    blog = db.relationship('Blog', back_populates='introduction')

    def __repr__(self):
        return f"Introduction-blog_id {self.blog_id} {self.hook}"
    
    def to_dict(self):
        return {
            # "id": self.id,
            # "blog_id": self.blog_id,
            "hook": self.hook,
            "purpose": self.purpose,
        }
