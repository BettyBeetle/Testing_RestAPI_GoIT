from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class ContactsIn(BaseModel):
    '''
    Data model for creating new contacts.

    Attributes:
        first_name (str): The first name of the contact. Must be between 4 and 16 characters.
        last_name (str): The last name of the contact. Must be between 4 and 16 characters.
        email (str): The email address of the contact.
        phone_number (str): The phone number of the contact.
        date_of_birth (date): The date of birth of the contact.
        nick (Optional[str]): An optional nickname of the contact.
    '''
    
    first_name: str = Field(min_length=4, max_length=16)
    last_name: str = Field(min_length=4, max_length=16)
    email: str
    phone_number: str
    date_of_birth: date
    nick: Optional[str]= None

class ContactsOut(ContactsIn):
    '''
    Data model for retrieving contacts.

    Attributes:
        id (int): The unique identifier of the contact.
        first_name (str): The first name of the contact. Must be between 4 and 16 characters.
        last_name (str): The last name of the contact. Must be between 4 and 16 characters.
        email (str): The email address of the contact.
        phone_number (str): The phone number of the contact.
        date_of_birth (date): The date of birth of the contact.
        nick (Optional[str]): An optional nickname of the contact.
    '''
    
    id: int

    class Config:
        orm_mode = True


class UserIn(BaseModel):
    '''
    Data model for creating new users.

    Attributes:
        username (str): The username of the user. Must be between 4 and 16 characters.
        email (str): The email address of the user.
        password (str): The password of the user. Must be between 6 and 10 characters.
    
    '''
    
    username: str = Field(min_length=4, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)

class UserOut(BaseModel):
    '''
    Data model for retrieving users.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        avatar (str): The avatar URL of the user.
    '''
    
    id: int
    username: str
    email: str
    avatar: str = "default_avatar.jpg"


    class Config:
        orm_mode = True

class TokenModel(BaseModel):
    '''
    Data model for tokens.

    Attributes:
        access_token (str): The access token.
        refresh_token (str): The refresh token.
        token_type (str): The type of token.
    '''
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    '''
    Data model for requesting email confirmation.

    Attributes:
        email (EmailStr): The email address for which confirmation is requested.
    
    '''
    
    email: EmailStr