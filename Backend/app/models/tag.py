from app import db
from sqlalchemy.sql import func
from datetime import datetime
from app.models.blog import blog_tags_association


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # blog_id = db.Column(db.Integer, db.ForeignKey('blog.id', ondelete='CASCADE'), nullable=False)    
    name = db.Column(db.String(50), unique=True, nullable=False)
    blogs = db.relationship(
        'Blog',
        secondary=blog_tags_association,
        backref=db.backref('tags_rel_backref', lazy='dynamic') # Menggunakan nama backref berbeda untuk menghindari konflik
    )
    def __repr__(self): return f"<Tag id={self.id} name='{self.name}'>"
    def to_dict(self): return {"name": self.name}

# class Tag(db.Model):
#     __tablename__ = 'tag'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     blog_id = db.Column(db.Integer, db.ForeignKey('blog.id', ondelete='CASCADE'), nullable=False)
#     tag_name = db.Column(db.String(100), nullable=False)
#     # Optional: hubungan balik ke user
#     blog = db.relationship('Blog', backref=db.backref('tag', lazy=True, cascade='all, delete-orphan'))

#     def __repr__(self):
#         return f"Tag-blog_id {self.blog_id} {self.tag_name}"
    
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "blog_id": self.blog_id,
#             "tag_name": self.tag_name,
#         }

