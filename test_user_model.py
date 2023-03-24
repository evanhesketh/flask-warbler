"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

bcrypt = Bcrypt()
PASSWORD = bcrypt.generate_password_hash("password", rounds=5).decode("utf-8")


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", PASSWORD, None)
        u2 = User.signup("u2", "u2@email.com", PASSWORD, None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)

    def test_user_is_following(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)
        u1.following.append(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))

    def test_user_is_not_following(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)
        self.assertFalse(u1.is_following(u2))

    def test_is_followed_by(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)
        u1.following.append(u2)
        db.session.commit()
        self.assertTrue(u2.is_followed_by(u1))

    def test_is_not_followed_by(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)
        self.assertFalse(u2.is_followed_by(u1))

    def test_user_signup(self):
        u = User.signup("named", "e@e.com", "password", None)
        db.session.commit()
        u = User.query.filter(User.username=="named").one_or_none()
        self.assertTrue(bcrypt.check_password_hash(u.password, "password"))
        self.assertTrue(u.username, "named")

    def test_user_signup_failure_no_name_given(self):
        # u = User.signup("u1", "f@e.com", "password", None)
        # db.session.commit()
        # u = User.query.filter(User.email=="f@e.com").one_or_none()
        # self.assertIsNone(u)
        # self.assertRaises(IntegrityError, User.signup("u1", "f@e.com", "password", None))
        # with pytest.raises(IntegrityError):
        #     User.signup("u1", "f@e.com", "password", None)


