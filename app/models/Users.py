from app.config.mysqlconnection import connectToMySQL


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.tipos_usuario_id = data['tipos_usuario_id']
        self.balance = data['balance']
        self.password = data['password']
        self.created_at = data['createdAt']
        self.updated_at = data['updatedAt']

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('exmaple_flask').query_db(query, {"email": email})
        user = None
        if len(results):
            user = cls(results[0])
        return user

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('exmaple_flask').query_db(query, {"id": id})
        user = None
        if len(results):
            user = cls(results[0])
        return user


    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, tipos_usuario_id, balance) values \
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(tipos_usuario_id)s, %(balance)s)"
        results = connectToMySQL('exmaple_flask').query_db(query, data)
        return results
