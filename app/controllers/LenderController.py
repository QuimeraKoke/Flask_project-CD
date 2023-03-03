from app.forms.LoanForm import LoanForm
from app.models.Loans import Loan
from app.models.Projects import Projects
from app.models.Users import User
from app.utils import LENDER_ID
from flask import render_template, redirect


def lender_controller(req, session):
    if ('user_id' in session):
        user = User.get_by_id(session['user_id'])
        if user.tipos_usuario_id != LENDER_ID:
            return redirect("/borrower")

        projects = Projects.get_all()
        projects = projects.values()

        my_projects = []
        other_projects = []

        for project in projects:
            project.calculate_raised_amount()

            flag = False
            for loan in project.loans:
                if loan.user_id == user.id:
                    project.my_lent = loan.amount
                    flag = True
                    break

            if (flag):
                my_projects.append(project)
            else:
                other_projects.append(project)

        return render_template(
            "lender.html",
            my_projects=my_projects,
            other_projects=other_projects,
            form=LoanForm(),
            user=user)
    return redirect("/")


def api_lend_controller(req, session):
    form = LoanForm(req.form)
    if ('user_id' in session):
        user = User.get_by_id(session['user_id'])
        if user.tipos_usuario_id != LENDER_ID:
            return redirect("/borrower")
        if (form.validate()):
            if (user.balance >= form.amount.data):
                # User.edit_balance()
                loan_data = {
                    'user_id': form.user_id.data,
                    'project_id': form.project_id.data,
                    'amount': form.amount.data
                }
                Loan.create(loan_data)
                return redirect("/lender")
            return redirect("/lender")
        return lender_controller(req, session)
    return redirect("/")
