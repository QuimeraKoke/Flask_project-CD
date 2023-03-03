from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField 
from wtforms.validators import Email, Length, InputRequired

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
        InputRequired(message="Debe ingresar un email valido"),
        Email(message="Debe ingresar un email válido"),
        Length(message="Su email debe tener mas de 5 cracteres", min=5)
    ], render_kw={'class': "form-control"})
    password = PasswordField("Password", validators=[
        InputRequired(message="Debe ingresar un email valido"),
        Length(message="Su clave debe tener entre 5 y 16 caracteres", min=5, max=16)
    ], render_kw={'class': "form-control"})