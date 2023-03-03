from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField


class LoanForm(FlaskForm):
    amount = IntegerField('amount')
    user_id = HiddenField('user_id')
    project_id = HiddenField('project_id')



