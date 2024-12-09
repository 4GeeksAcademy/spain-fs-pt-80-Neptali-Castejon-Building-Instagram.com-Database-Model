import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
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
    password = Column(String, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }

class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', backref='posts')

class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', backref='comments')
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Posts', backref='comments')

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content
        }

class Medias(Base):
    __tablename__ = 'medias'
    id = Column(Integer, primary_key=True)
    src = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Posts', backref='medias')

class Followers(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True)
    from_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    to_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    from_user = relationship('Users', foreign_keys=[from_user_id], backref='following')
    to_user = relationship('Users', foreign_keys=[to_user_id], backref='followers')

# Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
