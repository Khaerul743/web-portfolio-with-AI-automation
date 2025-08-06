from app import db
from sqlalchemy.sql import func
from datetime import datetime

class Body(db.Model):
    __tablename__ = 'body'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id', ondelete='CASCADE'), nullable=False, unique=True)
    conclusion = db.Column(db.Text, nullable=False)

    # hubungan balik ke blog (One-to-One)
    blog = db.relationship('Blog', back_populates='body')

    def __repr__(self):
        return f"Body-blog_id {self.blog_id} {self.conclusion}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "blog_id": self.blog_id,
            "conclusion": self.conclusion,
        } 