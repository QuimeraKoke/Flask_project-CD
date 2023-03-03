from app.config.mysqlconnection import connectToMySQL


class Loan:
    def __init__(self, data):
        self.id = data['id']
        self.project_id = data['project_id']
        self.user_id = data['user_id']
        self.amount = data['amount']
        self.created_at = data['createdAt']
        self.updated_at = data['updatedAt']

        self.user = None
        self.announcement = None

    @classmethod
    def create(cls, data):
        query = "INSERT INTO loans (amount, project_id, user_id) VALUES ( %(amount)s , %(project_id)s , %(user_id)s )"
        project_id = connectToMySQL('exmaple_flask').query_db(query, data)
        return project_id


