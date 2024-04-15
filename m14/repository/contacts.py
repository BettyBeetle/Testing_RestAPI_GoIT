from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, extract

from typing import List
from datetime import datetime, timedelta

from m14.database.models import User
from m14.database.models import Contacts
from m14.schemas import ContactsIn


async def upcoming_birthdays( user:User, db: Session) -> List[Contacts]:
    """
    Retrieves upcoming birthdays within the next 7 days for contacts.

    Args:
        db (Session): The database session to query.

    Returns:
        List[Contacts]: A list of contacts whose birthdays fall within the next 7 days.
    """


    today = datetime.now().date()
    end_date = today + timedelta(days=7)

    if today.month == end_date.month:
        contacts = db.query(Contacts).filter(
            extract('month', Contacts.date_of_birth) == today.month,
            extract('day', Contacts.date_of_birth) >= today.day,
            extract('day', Contacts.date_of_birth) <= end_date.day
        ).all()
    else:
        contacts = db.query(Contacts).filter(
            or_(
                and_(
                    extract('month', Contacts.date_of_birth) == today.month,
                    extract('day', Contacts.date_of_birth) >= today.day
                ),
                and_(
                    extract('month', Contacts.date_of_birth) == end_date.month,
                    extract('day', Contacts.date_of_birth) <= end_date.day
                )
            )
        ).all()
    return contacts


async def create_contact(body: ContactsIn, user:User, db: Session) -> Contacts:
    '''
    Creates a new contact for the specified user.

    Args:
        body (ContactsIn): The contact details to create.
        user (User): The user for whom the contact is being created.
        db (Session): The database session to use.

    Returns:
        Contacts: The newly created contact.
    '''

    contact = Contacts(
        first_name = body.first_name,
        last_name = body.last_name,
        email = body.email,
        phone_number = body.phone_number,
        date_of_birth = body.date_of_birth,
        nick = body.nick,
        user_id=user.id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_contacts(skip: int, limit: int, user:User, db: Session) -> List[Contacts]:
    '''
    Retrieves a list of contacts for the specified user with pagination.

    Args:
        skip (int): The number of contacts to skip.
        limit (int): The maximum number of contacts to retrieve.
        user (User): The user whose contacts are being retrieved.
        db (Session): The database session to query.

    Returns:
        List[Contacts]: A list of contacts belonging to the specified user
    '''

    return db.query(Contacts).filter(Contacts.user_id == user.id).offset(skip).limit(limit).all()


async def search_contacts(search: str, skip: int, limit: int, current_user: User, db: Session):
    '''
    Searches contacts based on the keyword in first name, last name, and email with pagination.

    Args:
        search (str): The keyword to search for.
        skip (int): Number of contacts to skip at the beginning of the list.
        limit (int): Maximum number of contacts to retrieve.
        db (Session): The database session to use for queries.

    Returns:
        List[Contacts]: A list of contacts matching the search criteria,
        starting from the contact at index 'skip' and retrieving at most 'limit' contacts.
    '''
    
    query = db.query(Contacts).filter(Contacts.user_id == current_user.id)
    if search:
        print("Applying search filters")
        query = query.filter(
            or_(
                Contacts.first_name.ilike(f"%{search}%"),
                Contacts.last_name.ilike(f"%{search}%"),
                Contacts.email.ilike(f"%{search}%")
            )
        )
    contacts = query.offset(skip).limit(limit).all()
    return contacts


async def get_contact(contact_id: int, user:User, db: Session) -> Contacts:
    '''
    Retrieves the contact with the specified ID for the given user.

    Args:
        contact_id (int): The ID of the contact to retrieve.
        user (User): The user whose contact is being retrieved.
        db (Session): The database session to use for queries.

    Returns:
        Contacts: The contact belonging to the specified user with the given ID.
    '''
    
    return db.query(Contacts).filter(and_(Contacts.id == contact_id, Contacts.user_id == user.id)).first()


async def update_contact(contact_id: int, body: ContactsIn,  user:User, db: Session) -> Contacts | None:
    '''
    Updates an existing contact for the specified user.

    Args:
        contact_id (int): The ID of the contact to update.
        body (ContactsIn): The updated contact details.
        user (User): The user who owns the contact being updated.
        db (Session): The database session to use for queries.

    Returns:
        Union[Contacts, None]: The updated contact if found and updated successfully,
        otherwise None.
    '''

    contact = db.query(Contacts).filter(and_(Contacts.id == contact_id, Contacts.user_id == user.id)).first()
    if contact:
        if body.first_name:
            contact.first_name = body.first_name
        if body.last_name:
            contact.last_name = body.last_name
        if body.email is not None:
            contact.email = body.email
        if body.phone_number:
            contact.phone_number = body.phone_number
        if body.date_of_birth:
            contact.date_of_birth = body.date_of_birth
        if body.nick is not None:
            contact.nick = body.nick
        db.commit()
        return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contacts | None:
    '''
       Removes an existing contact for the specified user.

    Args:
        contact_id (int): The ID of the contact to remove.
        user (User): The user who owns the contact.
        db (Session): The database session to use for queries.

    Returns:
        Union[Contacts, None]: The removed contact if found and successfully deleted,
        otherwise None.
    '''
    
    contact = db.query(Contacts).filter(and_(Contacts.id == contact_id, Contacts.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
