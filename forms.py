from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SelectMultipleField
from wtforms.validators import Required, Email, EqualTo


class RegisterForm(Form):
    foods = TextField('Foods', validators = [Required()])
    email = TextField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[Required()])
    confirm = PasswordField(
        'Confirm Password',
        validators=[Required(),
                    EqualTo('password', message='Passwords do not match.')])

    def validate(self):
        if not Form.validate(self):
            return False

        # TODO: Make sure that the user does not exist
        return True


class LoginForm(Form):
    email = TextField('Email', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
