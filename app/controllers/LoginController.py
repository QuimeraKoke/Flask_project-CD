from app.utils import LENDER_ID
import bcrypt
from app.models.Users import User
from flask import render_template, redirect

from app.forms.LoginForm import LoginForm


def login_controller(req, session):
    return render_template("login.html", login_form=LoginForm())

def api_login_controller(req, session):
    form = LoginForm(req.form)
    if form.validate():
        user = User.get_by_email(form.email.data)
        if (user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8'))):
            session['user_type'] = user.tipos_usuario_id
            session['user_id'] = user.id
            redirect_url = "/borrower"
            if user.tipos_usuario_id == LENDER_ID:
                redirect_url = "/lender"

            return redirect(redirect_url)
        else:
            form.password.errors.append('The password or the email is wrong')
    return render_template("login.html", login_form=form)

def logout_controller(req, session):
    session.clear()
    return redirect("/")

