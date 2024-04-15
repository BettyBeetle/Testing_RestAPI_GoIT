from sqlalchemy import Column, Integer, String, func, ForeignKey, Boolean
from sqlalchemy.sql.sqltypes import DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Contacts(Base):
    """
    SQLAlchemy model representing a table of contacts.

    Attributes:
        id (int): The unique identifier for each contact.
        first_name (str): The first name of the contact.
        last_name (str): The last name of the contact.
        email (str, optional): The email address of the contact (nullable).
        phone_number (str): The phone number of the contact.
        date_of_birth (datetime.date, optional): The date of birth of the contact (nullable).
        nick (str, optional): The nickname of the contact (nullable, default is None).
        user_id (int): The foreign key referencing the user to whom this contact belongs.
        user (relationship): Relationship to the User model representing the owner of this contact.
    """

    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, index=True, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    nick = Column(String, nullable=True, default=None)
    user_id = Column("user_id", ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", backref="contacts")


class User(Base):
    """
    SQLAlchemy model representing a table of users.

    Attributes:
        id (int): The unique identifier for each user.
        username (str): The username of the user.
        email (str): The email address of the user (nullable).
        confirmed (bool): Flag indicating whether the user's email address is confirmed.
        password (str): The password of the user. Note: It's recommended to store passwords hashed for security reasons.
        created_at (datetime): The timestamp indicating when the user account was created.
        avatar (str, optional): The URL or path to the user's avatar image (nullable).
        refresh_token (str, optional): The refresh token associated with the user (nullable).
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True,  autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)