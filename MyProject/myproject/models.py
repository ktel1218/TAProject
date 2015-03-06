from sqlalchemy import (
    Table,
    Column,
    Index,
    Integer,
    Text,
    String,
    ForeignKey,
    DateTime,
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

from sqlalchemy.orm import (
    relationship,
    scoped_session,
    sessionmaker,
    mapper,
    )

from pyramid.security import (
    Allow,
    Authenticated,
    Everyone,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from datetime import datetime

import transaction

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

# class Model(object):
#     """Base piece of content."""

#     __tablename__ = None

#     @property
#     def __name__(self):
#         return self.slug

#     @property
#     def __acl__(self):
#         """Permissions."""

#         return [(Allow, Everyone, 'view'),
#                 (Allow, 'group:editors', ('edit', 'add', 'delete')),
#         ]

# class Expert(Model, Base):
#     """Zana expert."""

#     __tablename__ = 'experts'
#     dbsession = DBSession

#     @reify
#     def __parent__(self):
#         from .expertsfolder import experts_folder

#         return experts_folder

#     __cms__ = [
#         Action('View', '', 'view'),
#         Action('Debug', '@@debug', 'edit'),
#         Action('Edit', '@@edit', 'edit'),
#         Action('Delete', '@@delete', 'delete'),
#         Action('Add Expert', '../@@add', 'add'),
#     ]
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(String(60), nullable=False)
    password = Column(String(30), nullable=False)
    social_score = Column(Integer, default=0)


class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    time = Column(DateTime, default=datetime.now())

    owner = relationship("User")


    def __init__(self, request):
        self.user_id = request.authenticated_userid
        self.time = datetime.now()
        self.__acl__ = [ (Allow, self.owner, 'view'), ]
    


class Idea(object):
    def __init__(self, request):
        pass

class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class UserStatus(Base):
    __tablename__ = 'userstatus'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    status_id = Column(Integer, ForeignKey('status.id'), primary_key=True)

    user = relationship("User", backref="user_status")
    movie = relationship("Status", backref="user_status")




class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    receiver_id = Column(Integer)
    time = Column(DateTime, default=datetime.now())



class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    parent_id = Column(Integer, ForeignKey('posts.id'))
    topic_id = Column(Integer, ForeignKey('topics.id'))



class Topic(Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(30), unique=True)
    description = Column(Text)




class RootFactory(object):
    __acl__ = [ (Allow, Authenticated, 'view'),
                # (Allow, Everyone, 'view'),
                (Allow, 'group:editors', 'edit') ]
    def __init__(self, request):
        pass



