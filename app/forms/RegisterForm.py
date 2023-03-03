from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import Email, Length, InputRequired, EqualTo, NumberRange


class BorrowerRegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        InputRequired(message="Debe ingresar un nombre valido"),
        Length(message="The first name should be at least 2 charactes min. and 255 max.", min=2, max=255)

    ], render_kw={'class': "form-control"})
    last_name = StringField('Last Name', validators=[
        InputRequired(message="Debe ingresar un nombre valido"),
        Length(message="The first name should be at least 2 charactes min. and 255 max.", min=2, max=255)

    ], render_kw={'class': "form-control"})
    email = StringField('Email', validators=[
        InputRequired(message="Debe ingresar un email valido"),
        Email(message="Debe ingresar un email válido"),
        Length(message="Su email debe tener mas de 5 cracteres", min=5)
    ], render_kw={'class': "form-control"})
    password = PasswordField('Password', validators=[
        InputRequired(message="Debe ingresar un email valido"),
        Length(message="Su clave debe tener entre 5 y 16 caracteres", min=5, max=16),
        EqualTo('confirm_password')
    ], render_kw={'class': "form-control"})
    confirm_password = PasswordField('Confirm password', validators=[
        InputRequired(message="Debe ingresar un email valido"),
        Length(message="Su clave debe tener entre 5 y 16 caracteres", min=5, max=16)
    ], render_kw={'class': "form-control"})


class LenderRegisterForm(BorrowerRegisterForm):
    money = IntegerField("Money (USD)", validators=[
        InputRequired(message="Este campo es necesario"),
        NumberRange(message="El monto debe ser mayor a 1 USD", min=1)
    ], render_kw={'class': "form-control"})
