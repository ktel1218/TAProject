from sqlalchemy import (
    Table,
    Column,
    Index,
    Integer,
    Text,
    String,
    ForeignKey,
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

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


# association table
user_status_table = Table('userstatus', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('status', Integer, ForeignKey('status.name'), primary_key=True)
)


def _return_status(name):
    """returns matching role"""
    # return UserStatus(name)
    status_match = DBSession.query(Status).filter_by(name=name).first()
    user_status_match = DBSession.query(UserStatus).filter_by(status=name).filter_by(user_id=1).first()
    if not status_match:
        raise NewStatus
    if not user_status_match:
        return UserStatus(1, name)
class NewStatus(Exception):
    """ Trying to add a new status to a user, generate new status first """
    pass
_return_status.NewStatus = NewStatus





class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    # phone = Column(String(20))
    email = Column(String(60), nullable=False)
    # phone_email = Column(String(20), nullable=False)
    password = Column(String(30), nullable=False)

    # status_assn_obj = relationship('Status', viewonly=True, secondary=lambda: user_status)
    
    statuses = association_proxy('user_status', 'status', creator=_return_status)
Index('user_index', User.name, unique=True, mysql_length=255)




class Status(Base):
    __tablename__ = "status"
    name = Column(Text, primary_key=True)

    def __init__(self, name):
        self.name = name


class UserStatus(object):
    def __init__(self, user_id=None, status=None):
        self.user_id = user_id
        self.status = status

mapper(UserStatus, user_status_table, properties={
    '_user': relationship(User, backref='user_status'),
    '_status': relationship(Status),
})













class Topic(Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    description = Column(Text, nullable=False)#number long?)



class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    topic_id = Column(Integer)






class RootFactory(object):
    __acl__ = [ (Allow, Authenticated, 'view'),
                # (Allow, Everyone, 'view'),
                (Allow, 'group:editors', 'edit') ]
    def __init__(self, request):
        pass



