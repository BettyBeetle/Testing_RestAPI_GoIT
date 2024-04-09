from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, extract

from typing import List
from datetime import datetime, timedelta

from m14.database.models import User
from m14.database.models import Contacts
from m14.schemas import ContactsIn


async def upcoming_birthdays( user:User, db: Session) -> List[Contacts]:
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
    return db.query(Contacts).filter(Contacts.user_id == user.id).offset(skip).limit(limit).all()

async def search_contacts(search: str, skip: int, limit: int, current_user: User, db: Session):
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
    return db.query(Contacts).filter(and_(Contacts.id == contact_id, Contacts.user_id == user.id)).first()


async def update_contact(contact_id: int, body: ContactsIn,  user:User, db: Session) -> Contacts | None:
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
    contact = db.query(Contacts).filter(and_(Contacts.id == contact_id, Contacts.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
