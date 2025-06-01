class User:
    def __init__(self, username, password, role, phone=None, email=None):
        self.username = username
        self.password = password
        self.role = role
        self.phone = phone
        self.email = email