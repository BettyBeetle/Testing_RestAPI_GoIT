import pickle

from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from m14.database.db import get_db
from m14.database.models import User
from m14.repository import users as repository_users
from m14.services.auth import auth_service, Auth
from m14.conf.config import settings
from m14.schemas import UserOut

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    '''
    Retrieve the details of the currently authenticated user.

    Args:
        current_user (User): The currently authenticated user.

    Returns:
        UserOut: Details of the currently authenticated user.
    '''
    
    return current_user


@router.patch('/avatar', response_model=UserOut)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    '''
    Update the avatar for the currently authenticated user.

    Args:
        file (UploadFile): The avatar image file to upload.
        current_user (User): The currently authenticated user.
        db (Session): The database session.

    Returns:
        UserOut: The updated details of the currently authenticated user.
    '''
    
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    r = cloudinary.uploader.upload(file.file, public_id=f'NotesApp/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'NotesApp/{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    Auth.r.set(f"user:{user.email}", pickle.dumps(user))
    return user
