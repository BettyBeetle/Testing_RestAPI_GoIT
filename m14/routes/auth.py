from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from fastapi.requests import Request
from sqlalchemy.orm import Session

from m14.database.db import get_db
from m14.schemas import UserIn, UserOut, TokenModel, RequestEmail
from m14.repository import users as repository_users
from m14.services.auth import auth_service
from m14.services.email_service import send_email


router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)

async def signup(body: UserIn, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    '''
    Handles POST request to the "/signup" endpoint, creating a new user in the system.

    Args:
        body (UserIn): Input data for creating the user.
        background_tasks (BackgroundTasks): Background tasks to execute, e.g., sending emails.
        request (Request): The request object.

        db (Session, optional): The database session.

    Returns:
        UserOut: Data of the newly created user.

    Raises:
        HTTPException: If there is a conflict with an existing account or an internal server error occurs.
    
    '''
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email, new_user.email, new_user.username, request.base_url)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        print("Error while saving user to database:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error while saving user to database")
    return UserOut(id=new_user.id, username=new_user.username, email=new_user.email)
    

@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    '''
    Handles the login process for a existing users.

    Args:
        body (OAuth2PasswordRequestForm): The credentials used for authentication.
        db (Session): The database session.

    Returns:
        TokenModel: The access and refresh tokens upon successful login.

    Raises:
        HTTPException: If the provided email is invalid, email is not confirmed, or password is incorrect.
    '''
    
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return TokenModel(access_token=access_token, refresh_token=refresh_token)


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    '''
    Refreshes the access token using the refresh token for authenticated users.

    Args:
        credentials (HTTPAuthorizationCredentials): The HTTP authorization credentials containing the refresh token. 
        db (Session): The database session.

    Returns:
        TokenModel: The new access and refresh tokens.

    Raises:
        HTTPException: If the refresh token is invalid or expired.
    '''
    
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    '''
    Confirm the email address associated with the provided token.

    Args:
        token (str): The verification token.
        db (Session, optional): The database session.

    Returns:
        dict: A message indicating the status of email confirmation.

    Raises:
        HTTPException: If the token is invalid or email confirmation fails.
    '''

    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirm_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    '''
    Request confirmation email for the provided email address.

    Args:
        body (RequestEmail): The email address for which confirmation is requested.
        background_tasks (BackgroundTasks): Background tasks to execute, e.g., sending emails.
        request (Request): The request object.
        db (Session, optional): The database session.

    Returns:
        dict: A message indicating the status of the email confirmation request.

    '''
    
    user = await repository_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, request.base_url)
    return {"message": "Check your email for confirmation."}