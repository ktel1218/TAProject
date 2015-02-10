from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from pyramid.security import (
    Allow,
    Authenticated,
    Everyone,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


# class MyModel(Base):
#     __tablename__ = 'models'
#     id = Column(Integer, primary_key=True)
#     name = Column(Text)
#     value = Column(Integer)

# Index('my_index', MyModel.name, unique=True, mysql_length=255)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    phone = Column(String(20))
    email = Column(String(60), nullable=False)
    password = Column(String(30), nullable=False)

Index('user_index', User.name, unique=True, mysql_length=255)

class Status(Base):
    __tablename__ = "statuses"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

class RootFactory(object):
    __acl__ = [ (Allow, Authenticated, 'view'),
                # (Allow, Everyone, 'view'),
                (Allow, 'group:editors', 'edit') ]
    def __init__(self, request):
        pass



