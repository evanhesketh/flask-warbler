"""User view function tests."""

# run these tests like:
#
#    python -m unittest test_user_views.py


from app import app
import os
from unittest import TestCase

from flask import session
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from models import db, User, Message, Like

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Don't req CSRF for testing
app.config['WTF_CSRF_ENABLED'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

bcrypt = Bcrypt()
PASSWORD = bcrypt.generate_password_hash("password").decode("utf-8")

USER_1 = {
    "username": "user-1",
    "password": PASSWORD,
    "email": "user-1@email.com"
}


class UserRoutesTestCase(TestCase):
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

    def test_homepage_logged_out(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("New to Warbler?", html)

    def test_homepage_logged_in(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["curr_user"] = self.u1_id
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@u1", html)

    def test_signup_form(self):
        with app.test_client() as client:
            resp = client.get('/signup')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Sign me up!", html)

    def test_signup_ok(self):
        with app.test_client() as client:
            resp = client.post(
                '/signup',
                data={
                    "username": "u3",
                    "password": "password",
                    "email": "u3@email.com"
                }
            )

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/")

            u3 = User.query.filter(User.username == "u3").first()

            self.assertTrue(bcrypt.check_password_hash(u3.password, "password"))
            self.assertEqual(session.get("curr_user"), u3.id)


