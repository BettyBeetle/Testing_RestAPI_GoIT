from sqlalchemy import Column, Integer, String, func, ForeignKey, Boolean
from sqlalchemy.sql.sqltypes import DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Contacts(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone_number = Column(String, index=True, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    nick = Column(String, nullable=True, default=None)
    user_id = Column("user_id", ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", backref="contacts")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,  autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    confirmed = Column(Boolean, default=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)