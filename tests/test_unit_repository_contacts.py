from datetime import datetime, timedelta
import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from m14.database.models import Contacts, User
from m14.schemas import ContactsIn
from m14.repository.contacts import (
    upcoming_birthdays,
    create_contact,
    get_contacts,
    search_contacts,
    get_contact,
    update_contact,
    remove_contact,
)

class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_upcoming_birthdays(self):
        today = datetime.now().date()
        end_date = today + timedelta(days=7)
        contacts = [
            Contacts(date_of_birth=today),
            Contacts(date_of_birth=end_date),
            Contacts(date_of_birth=today + timedelta(days=3)),
        ]
        self.session.query().filter().all.return_value = contacts

        result = await upcoming_birthdays(user=self.user, db=self.session)

        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        contact_input = ContactsIn(
            first_name="John",
            last_name="Dooe",
            email="john.doe@example.com",
            phone_number="123456789",
            date_of_birth="1990-01-01",
            nick="johnny"
        )
        result = await create_contact(body=contact_input, user=self.user, db=self.session)
        self.assertEqual(result.first_name, result.first_name)
        self.assertEqual(result.last_name, result.last_name)
        self.assertEqual(result.email, result.email)
        self.assertEqual(result.phone_number, result.phone_number)
        self.assertEqual(result.date_of_birth, result.date_of_birth)
        self.assertEqual(result.nick, result.nick)
        self.assertEqual(result.user_id, self.user.id)

        self.assertTrue(self.session.add.called)
        self.assertTrue(self.session.commit.called)


    async def test_get_contacts(self):
        contacts = [Contacts(), Contacts(), Contacts()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)


    async def test_search_contacts(self):
        search_query = "John"
        contacts = [
        Contacts(first_name="John"),
        Contacts(first_name="Jane"),
        ]
    
        self.session.query().filter().filter().offset().limit().all.return_value = contacts
        result = await search_contacts(search=search_query, skip=0, limit=10, current_user=self.user, db=self.session)
        self.assertEqual(result, contacts)


    async def test_get_contact_found(self):
        contact = Contacts()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)


    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)


    async def test_update_contact_found(self):
        contact_input = ContactsIn(
            first_name="John",
            last_name="Dooe",
            email="john.doe@example.com",
            phone_number="123456789",
            date_of_birth="1990-01-01",
            nick="johnny"
        )
        contact = Contacts(
            id=1,
            user_id=self.user.id,
            first_name="Old_First_Name",
            last_name="Old_Last_Name",
            email="old@example.com",
            phone_number="987654321",
            date_of_birth="1980-01-01",
            nick="old_nick"
        )
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=contact_input, user=self.user, db=self.session)
        self.assertEqual(result.first_name, result.first_name)
        self.assertTrue(self.session.commit.called)
        

    async def test_update_contact_not_found(self):
        contact_input = ContactsIn(
            first_name="John",
            last_name="Dooe",
            email="john.doe@example.com",
            phone_number="123456789",
            date_of_birth="1990-01-01",
            nick="johnny"
        )
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=contact_input, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_remove_contact_found(self):
        contact = Contacts()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)
        self.assertTrue(self.session.delete.called)
        self.assertTrue(self.session.commit.called)


    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
