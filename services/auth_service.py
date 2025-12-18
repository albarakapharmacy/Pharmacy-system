from db.database import Database

class AuthService:
    @staticmethod
    def login(username, password):
        db = Database()
        user = db.fetch_all(
            'SELECT * FROM users WHERE username=? AND password=?',
            (username, password)
        )
        return user[0] if user else None
