"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py

from app import app
import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from models import db, User, Message, Like

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

db.drop_all()
db.create_all()

class MessageModelTestCase(TestCase):
    def setUp(self):
        Like.query.delete()
        User.query.delete()
        Message.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        message1 = Message(text="New Message", user_id=self.u1_id)

        db.session.add(message1)
        db.session.commit()
        self.message1_id = message1.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_message_model(self):
        message1 = Message.query.get(self.message1_id)

        self.assertEquals("New Message", message1.text)
        self.assertEquals(self.u1_id, message1.user_id)

    def test_message_model_failure(self):
        with self.assertRaises(IntegrityError):
            message = Message(text=None, user_id=self.u1_id)
            db.session.add(message)
            db.session.commit()

    def test_message_likes(self):
        message = Message.query.get(self.message1_id)
        new_like = Like(message_id=message.id, user_id=self.u2_id)

        db.session.add(new_like)
        db.session.commit()

        u2 = User.query.get(self.u2_id)

        self.assertTrue(message.likes[0].id, u2.id)




