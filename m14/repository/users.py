from libgravatar import Gravatar
from sqlalchemy.orm import Session

from m14.database.models import User
from m14.schemas import UserIn, UserOut


async def get_user_by_email(email: str, db: Session) -> UserOut:
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserIn, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()


async def confirm_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> UserOut:
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
