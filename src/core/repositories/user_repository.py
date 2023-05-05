from abc import ABC, abstractmethod
from typing import Optional

from core.entities.users.user import User


class UserRepository(ABC):
    # -------------------------------------- Retrieve -------------------------- #
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        pass
