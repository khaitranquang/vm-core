from core.entities.users.user import User
from core.exceptions.user_exception import UserDoesNotExistException
from core.repositories.user_repository import UserRepository


class UserService:
    """
    This class represents Use Cases related to User
    """

    def __init(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_by_id(self, user_id: str) -> User:
        user = self.user_repository.get_user_by_id(user_id=user_id)
        if not user:
            raise UserDoesNotExistException
        return user
