import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String, nullable=False, unique=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }

class Followers(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_to_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_from = relationship('Users', foreign_keys=[user_from_id], backref='following')
    user_to = relationship('Users', foreign_keys=[user_to_id], backref='followers')

class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', backref='comments')
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Posts', backref='comments')
    comment_text = Column(String, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text
        }
    
class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

class Medias(Base):
    __tablename__ = 'medias'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    type = Column(Enum('image', 'video', 'audio', name='media_types'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Posts', backref='medias')

# Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
