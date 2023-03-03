from app.controllers.BorrowerController import borrower_controller
from app.controllers.LenderController import api_lend_controller, lender_controller
from app.controllers.RegisterController import api_register_borrower_controller, api_register_lender_controller, register_controller
from flask import request, session

from app import app
from app.controllers.LoginController import api_login_controller, login_controller, logout_controller


@app.route("/")
def login():
    return login_controller(request, session)

@app.route("/register")
def register():
    return register_controller(request, session)

@app.route("/lender")
def lender():
    return lender_controller(request, session)

@app.route("/borrower")
def borrower():
    return borrower_controller(request, session)

@app.route("/logout")
def logout():
    return logout_controller(request, session)

# API 

@app.route("/api/lender/register", methods=['POST'])
def api_register_lender():
    return api_register_lender_controller(request, session)

@app.route("/api/borrower/register", methods=['POST'])
def api_register_borrower():
    return api_register_borrower_controller(request, session)

@app.route("/api/login", methods=['POST'])
def api_login():
    return api_login_controller(request, session)

@app.route("/api/lend", methods=['POST'])
def api_lend():
    return api_lend_controller(request, session)
