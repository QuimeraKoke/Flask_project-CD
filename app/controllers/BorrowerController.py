from app.models.Projects import Projects
from app.models.Users import User
from app.utils import BORROWER_ID
from flask import render_template, redirect

def borrower_controller(req, session):
    if ('user_id' in session):
        user = User.get_by_id(session['user_id'])
        if user.tipos_usuario_id != BORROWER_ID:
            return redirect("/lender")
        project = Projects.get_all_from_user(user.id)
        amount_raised = 0
        for loan in project.loans:
            amount_raised += loan.amount
        return render_template("borrower.html", user=user, amount_raised=amount_raised, project=project)
    return redirect("/")