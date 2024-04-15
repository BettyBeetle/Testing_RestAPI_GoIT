import unittest
from unittest import mock
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from m14.database.models import User
from m14.schemas import UserIn
from m14.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirm_email,
    update_avatar,
)

class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)


    async def test_get_user_by_email_found(self):
        email = "test@example.com"
        user = User(email=email)
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email=email, db=self.session)
        self.assertEqual(result, user)


    @patch("libgravatar.Gravatar.get_image", side_effect=Exception)
    async def test_create_user(self, mock_gravatar):
        user_in = UserIn(
            email="test@example.com",
            username="test_user",
            password="pass123",
            name="Test User"
        )
        with self.assertRaises(Exception):
            await create_user(user_in)


    async def test_get_user_by_email_not_found(self):
        email = "test@example.com"
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email=email, db=self.session)
        self.assertIsNone(result)


    async def test_update_token(self):
        user = User(email="test@example.com")
        token = "test_token"
        user.refresh_token = None
        await update_token(user=user, token=token, db=self.session)
        self.assertEqual(user.refresh_token, token)


    async def test_confirm_email(self):
        email = "test@example.com"
        user = User(email=email, confirmed=False)
        self.session.query().filter().first.return_value = user
        await confirm_email(email=email, db=self.session)
        self.assertTrue(user.confirmed)


    async def test_update_avatar(self):
        email = "test@example.com"
        url = "http://example.com/avatar.jpg"
        user = User(email=email)
        self.session.commit = MagicMock(return_value=None)
        updated_user = await update_avatar(email=email, url=url, db=self.session)
        self.assertEqual(updated_user.avatar, url)


if __name__ == '__main__':
    unittest.main()

