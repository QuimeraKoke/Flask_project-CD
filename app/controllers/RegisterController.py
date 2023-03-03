from app.models.Projects import Projects
from app.models.Users import User
from app.utils import BORROWER_ID, LENDER_ID
from flask import render_template, redirect
import bcrypt

from app.forms.ProjectForm import ProjectForm
from app.forms.RegisterForm import BorrowerRegisterForm, LenderRegisterForm

def register_controller(req, session):
    return render_template(
        "register.html", 
        lender_form=LenderRegisterForm(), 
        borrower_form=BorrowerRegisterForm(),
        project_form=ProjectForm()
        )

def api_register_lender_controller(req, session):
    form = LenderRegisterForm(req.form)
    if form.validate():
        encripted_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt(10))
        user_data = {
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "email": form.email.data,
            "tipos_usuario_id": LENDER_ID,
            "password": encripted_password,
            "balance": form.money.data
        }
        user_id = User.create(user_data)
        return redirect("/")
    return render_template(
        "register.html", 
        lender_form=form, 
        borrower_form=BorrowerRegisterForm(),
        project_form=ProjectForm()
        )


def api_register_borrower_controller(req, session):
    form_user = BorrowerRegisterForm(req.form)
    project_form = ProjectForm(req.form)
    if form_user.validate() and project_form.validate():
        encripted_password = bcrypt.hashpw(form_user.password.data.encode('utf-8'), bcrypt.gensalt(10))
        user_data = {
            "first_name": form_user.first_name.data,
            "last_name": form_user.last_name.data,
            "email": form_user.email.data,
            "tipos_usuario_id": BORROWER_ID,
            "password": encripted_password,
            "balance": 0
        }
        user_id = User.create(user_data)
        project_data = {
            'user_id': user_id,
            'title': project_form.title.data,
            'description': project_form.description.data,
            'amount': project_form.amount.data
        }
        Projects.create(project_data)
        return redirect("/")
    return render_template(
        "register.html", 
        lender_form=LenderRegisterForm(), 
        borrower_form=form_user,
        project_form=project_form
        )
    