from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, URL, Optional, ValidationError


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField(
        'Username',
        validators=[DataRequired()],
    )

    email = StringField(
        'E-mail',
        validators=[DataRequired(), Email()],
    )

    password = PasswordField(
        'Password',
        validators=[Length(min=6)],
    )

    image_url = StringField(
        '(Optional) Image URL',
        validators=[Optional(), URL()]
    )


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        'Username',
        validators=[DataRequired()],
    )

    password = PasswordField(
        'Password',
        validators=[Length(min=6)],
    )


def validate_img_url(self, field):
    """Raises URL validation error if invalid URL and not default image. """
    print('input', field.data)
    if (field.data != '/static/images/default-pic.png' and
            field.data != '/static/images/warbler-hero.jpg'):
        raise ValidationError('Please enter a valid URL')


class UserUpdateForm(FlaskForm):
    """Form for adding users."""

    username = StringField(
        'Username',
        validators=[DataRequired()],
    )

    email = StringField(
        'E-mail',
        validators=[DataRequired(), Email()],
    )

    location = StringField(
        '(Optional) Location',
    )

    image_url = StringField(
        '(Optional) Image URL',
        validators=[Optional(), validate_img_url]
    )

    header_image_url = StringField(
        '(Optional) Image URL',
        validators=[Optional(), validate_img_url]
    )

    bio = TextAreaField(
        '(Optional) Bio',
    )

    password = PasswordField(
        'Password',
        validators=[Length(min=6)],
    )


class CsrfForm(FlaskForm):
    """CSRF form."""
