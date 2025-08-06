from app import db
from sqlalchemy.sql import func
from datetime import datetime


blog_tags_association = db.Table(
    'blog_tags_association',
    db.Column('blog_id', db.Integer, db.ForeignKey('blog.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    headline = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.String(255), nullable=False)
    read_time = db.Column(db.Integer, default=0)
    accepted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    introduction = db.relationship('Introduction', back_populates='blog', uselist=False, cascade='all, delete-orphan')
    body = db.relationship('Body', back_populates='blog', uselist=False, cascade='all, delete-orphan')
    tags = db.relationship(
        'Tag',
        secondary=blog_tags_association,
        backref=db.backref('blogs_backref', lazy='dynamic') # Menggunakan nama backref berbeda untuk menghindari konflik
    )
    def __repr__(self): return f"<Blog id={self.id} title='{self.title[:30]}...' accepted={self.accepted}>"
    def to_dict(self, include_tags=True):
        data = {
            "id": self.id,
            "title": self.title,
            "headline": self.headline,
            "author": self.author,
            "description": self.description,
            "thumbnail": self.thumbnail,
            "read_time": self.read_time,
            # "accepted": self.accepted,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            # "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_tags:
            data["tags"] = [tag.to_dict() for tag in self.tags] # Langsung iterasi self.tags
        return data
    
# class Blog(db.Model):
#     __tablename__ = "blog"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     thumbnail = db.Column(db.String(100), nullable=False)
#     read_time = db.Column(db.Integer, default=0) 
#     accepted = db.Column(db.Boolean, default=False)
#     created_at = db.Column(db.DateTime, default=datetime.now)
#     updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
#     def __repr__(self):
#         return f"blog {self.title}"

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "title": self.title,
#             "description": self.description,
#             "thumbnail": self.thumbnail,
#             "read_time": self.read_time,
#             "accepted": self.accepted,
#             "created_at": self.created_at.isoformat() if self.created_at else None,
#             "updated_at": self.updated_at.isoformat() if self.updated_at else None,
#         } 