from app.config.mysqlconnection import connectToMySQL
from app.models.Loans import Loan
from app.models.Users import User


class Projects:
    def __init__( self, data ):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.amount = data['amount']
        self.user_id = data['user_id']
        self.created_at = data['createdAt']
        self.updated_at = data['updatedAt']

        self.user = None
        self.loans = []
        self.raised = 0
        self.my_lent = 0


    @classmethod
    def get_all_from_user(cls, user_id):
        query = "SELECT * FROM projects LEFT JOIN loans ON projects.id = loans.project_id LEFT JOIN users ON loans.user_id = users.id WHERE projects.user_id = %(user_id)s"
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL('exmaple_flask').query_db(query, {'user_id': user_id})
        if (len(results) == 0):
            return None
        print(results[0].keys())
        project_data = {
            'id': results[0]['id'],
            'title': results[0]['title'],
            'description': results[0]['description'],
            'amount': results[0]['amount'],
            'user_id': results[0]['user_id'],
            'createdAt': results[0]['createdAt'],
            'updatedAt': results[0]['updatedAt'],
        }
        project = cls(project_data)
        for result in results:
            if result['loans.id'] is None:
                break
            loan_data = {
                'id': result['loans.id'],
                'project_id': result['project_id'],
                'user_id': result['loans.user_id'],
                'amount': result['loans.amount'],
                'createdAt': result['loans.createdAt'],
                'updatedAt': result['loans.updatedAt'],
            }
            loan = Loan(loan_data)
            user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": result['password'],
                "tipos_usuario_id": result['tipos_usuario_id'],
                "balance": result['balance'],
                "createdAt": result['users.createdAt'],
                "updatedAt": result['users.updatedAt'],
            }
            loan.user = User(user_data)
            project.loans.append(loan)
        return project
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM projects LEFT JOIN loans ON projects.id = loans.project_id LEFT JOIN users ON projects.user_id = users.id"
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL('exmaple_flask').query_db(query)
        if (len(results) == 0):
            return None
        projects = {}
        for result in results:
            # Si el proyecto NO esta guardado en el diccionario lo creamos para usarlo posteriormente
            if not result['id'] in projects:
                project_data = {
                'id': result['id'],
                'title': result['title'],
                'description': result['description'],
                'amount': result['amount'],
                'user_id': result['user_id'],
                'createdAt': result['createdAt'],
                'updatedAt': result['updatedAt'],
                }
                project = cls(project_data)
                user_data = {
                    "id": result['users.id'],
                    "first_name": result['first_name'],
                    "last_name": result['last_name'],
                    "email": result['email'],
                    "tipos_usuario_id": result['tipos_usuario_id'],
                    "password": result['password'],
                    "balance": result['balance'],
                    "createdAt": result['users.createdAt'],
                    "updatedAt": result['users.updatedAt'],
                }
                project.user = User(user_data)
                projects[result['id']] = project
            if result['loans.id'] is None:
                break
            loan_data = {
                'id': result['loans.id'],
                'project_id': result['project_id'],
                'user_id': result['loans.user_id'],
                'amount': result['loans.amount'],
                'createdAt': result['loans.createdAt'],
                'updatedAt': result['loans.updatedAt'],
            }
            loan = Loan(loan_data)
            projects[result['id']].loans.append(loan)
        return projects
        

    @classmethod
    def create(cls, data):
        query = "INSERT INTO projects (title, description, amount, user_id) VALUES ( %(title)s , %(description)s , %(amount)s , %(user_id)s )"
        project_id = connectToMySQL('exmaple_flask').query_db(query, data)
        return project_id
    
    def calculate_raised_amount(self):
        self.raised = 0
        for loan in self.loans:
            self.raised += loan.amount 
    

