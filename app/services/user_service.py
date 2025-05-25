from app.dao.user_dao import UserDAO
from app.models.user import User

class UserService:
    def get_users(self):
        return UserDAO.get_all()

    def get_user(self, user_id):
        return UserDAO.get_by_id(user_id)

    def create_user(self, data):
        user = User(**data)
        return UserDAO.create(user)

    def update_user(self, user_id, data):
        user = UserDAO.get_by_id(user_id)
        for key, value in data.items():
            setattr(user, key, value)
        UserDAO.update()
        return user

    def delete_user(self, user_id):
        user = UserDAO.get_by_id(user_id)
        UserDAO.delete(user)
