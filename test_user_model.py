"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase

from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from models import db, User, Message, Like

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

bcrypt = Bcrypt()
HASHED_PASSWORD = bcrypt.generate_password_hash("password").decode("utf-8")

DEFAULT_IMAGE_URL = "/static/images/default-pic.png"
DEFAULT_HEADER_IMAGE_URL = "/static/images/warbler-hero.jpg"


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        u1 = User.query.get(self.u1_id)

        # Test all attributes after User instantiation
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)
        self.assertEqual(len(u1.liked_messages), 0)
        self.assertEqual(u1.email, "u1@email.com")
        self.assertEqual(u1.username, "u1")
        self.assertEqual(u1.image_url, DEFAULT_IMAGE_URL)
        self.assertEqual(u1.header_image_url, DEFAULT_HEADER_IMAGE_URL)
        self.assertTrue(bcrypt.check_password_hash(u1.password, 'password'))
        self.assertEqual(u1.bio, None)
        self.assertEqual(u1.location, None)

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
        u = User.query.filter(User.username == "named").one_or_none()
        self.assertTrue(bcrypt.check_password_hash(u.password, "password"))
        self.assertTrue(u.username, "named")

    def test_user_signup_failure_existing_username(self):
        with self.assertRaises(IntegrityError):
            User.signup("u1", "f@e.com", "password", None)
            db.session.commit()

    def test_user_signup_failure_no_username(self):
        with self.assertRaises(IntegrityError):
            User.signup(None, "f@e.com", "password", None)
            db.session.commit()

    def test_user_signup_failure_existing_email(self):
        with self.assertRaises(IntegrityError):
            User.signup("newuser", "u1@email.com", "password", None)
            db.session.commit()

    def test_user_signup_failure_no_email(self):
        with self.assertRaises(IntegrityError):
            User.signup("newuser", None, "password", None)
            db.session.commit()

    def test_user_signup_failure_no_password(self):
        with self.assertRaises(ValueError):
            User.signup("newuser", "e@e.com", None, None)

    def test_user_authenticate_sucess(self):
        user = User.authenticate("u1", "password")
        u1 = User.query.get(self.u1_id)

        self.assertEqual(user, u1)

    def test_user_authenticate_fail_invalid_username(self):
        user = User.authenticate("notthere", "password")

        self.assertFalse(user)

    def test_user_authenticate_fail_invalid_password(self):
        user = User.authenticate("u1", "12345")

        self.assertFalse(user)

    def test_user_has_liked_true(self):
        new_message = Message(text="new messaage", user_id=self.u1_id)

        db.session.add(new_message)
        db.session.commit()

        new_like = Like(message_id=new_message.id, user_id=self.u2_id)

        db.session.add(new_like)
        db.session.commit()

        u2 = User.query.get(self.u2_id)

        self.assertTrue(u2.has_liked(new_message), True)

    def test_user_has_liked_false(self):
        new_message = Message(text="new messaage", user_id=self.u1_id)

        db.session.add(new_message)
        db.session.commit()

        u2 = User.query.get(self.u2_id)

        self.assertFalse(u2.has_liked(new_message), False)


