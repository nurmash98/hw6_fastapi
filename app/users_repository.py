from attrs import define
from jose import jwt

@define
class User:
    email: str
    full_name: str
    password: str
    id: int = 0


class UsersRepository:
    users: list[User]

    def __init__(self):
        self.users = []

    # необходимые методы сюда
    def save(self, email, full_name, password):
        id = len(self.users) + 1
        self.users.append(User(email = email, full_name = full_name, id = id, password=password))
    
    def getAll(self):
        print (self.users)
        
    def get_by_email(self, email):
        for user in self.users:
            if email == user.email:
                return user
            
        return None
    def get_by_id(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    

