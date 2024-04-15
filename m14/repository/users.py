from libgravatar import Gravatar
from sqlalchemy.orm import Session

from m14.database.models import User
from m14.schemas import UserIn, UserOut


async def get_user_by_email(email: str, db: Session) -> UserOut:
    '''
    Retrieve a user from the database by their email address.

    Args:
        email (str): The email address of the user to retrieve.
        db (Session): The database session.

    Returns:
        UserOut: The user retrieved from the database.
    '''
    
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserIn, db: Session) -> User:
    '''
     Create a new user in the database.

    Args:
        body (UserIn): The input data for creating the user.
        db (Session): The database session.

    Returns:
        User: The newly created user.

    Raises:
        Exception: If an error occurs while fetching the avatar from Gravatar.
    '''

    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    if avatar is None:
        pass
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    '''
     Update the refresh token for a given user in the database.

    Args:
        user (User): The user for whom the refresh token will be updated.
        token (str | None): The new refresh token. If None, the token will be removed.
        db (Session): The database session.

    Returns:
        None
    '''
    
    user.refresh_token = token
    db.commit()

async def confirm_email(email: str, db: Session) -> None:
    '''
    Confirm the email address of the user with the given email  in the database.

    Args:
        email (str): The email address of the user to confirm.
        db (Session): The database session.

    Returns:
        None
    '''
    
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> UserOut:
    '''
     Update the avatar URL for the user with the given email address in the database.

    Args:
        email (str): The email address of the user whose avatar will be updated.
        url (str): The new avatar URL.
        db (Session): The database session.

    Returns:
        UserOut: The user with the updated avatar URL.
    '''
    
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
