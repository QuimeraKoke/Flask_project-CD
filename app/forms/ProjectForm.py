from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import Email, Length, InputRequired, NumberRange


class ProjectForm(FlaskForm):
    title = StringField('Need money for', validators=[
        InputRequired(message="Este campo es necesario"),
        Length(message="Este campo es necesario", min=5),
    ], render_kw={'class': "form-control"})
    description = TextAreaField('Description', validators=[
        InputRequired(message="Este campo es necesario"),
        Length(message="Este campo es necesario", min=10),
    ], render_kw={'class': "form-control"})
    amount = IntegerField('Amount needed', validators=[
        InputRequired(message="Este campo es necesario"),
        NumberRange(message="El monto debe ser mayor a 1 USD", min=1)
    ], render_kw={'class': "form-control"})


