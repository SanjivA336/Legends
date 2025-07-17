from typing import Optional, List
from backend.database._database_core import database_manager
from backend.models import User

class UsersManager():
    """
    A class for managing user data in a Firestore database.
    """
    
    def __init__(self):
        self._db = database_manager
        self._collection = "users"

    # --- Core CRUD Operations ---
    def get_user(self, user_id: str) -> Optional[User]:
        data = self._db._get_document(self._collection, user_id)
        if data:
            return User(**data)
        return None

    def add_user(self, user: User) -> Optional[str]:
        return self._db._add_document(self._collection, user.model_dump())

    def update_user(self, user: User) -> bool:
        return self._db._update_document(self._collection, user.id, user.model_dump(exclude_unset=True))

    def delete_user(self, user_id: str) -> bool:
        return self._db._delete_document(self._collection, user_id)

    def get_all_users(self, limit: Optional[int] = None) -> List[User]:
        user_dicts = self._db._list_documents(self._collection, limit)
        return [User(**data) for data in user_dicts if data]  # Filter out any None values

    def query_users(self, filters: List[tuple], limit: Optional[int] = None) -> List[User]:
        user_dicts = self._db._query_collection(self._collection, filters, limit)
        return [User(**data) for data in user_dicts if data]  # Filter out any None values
    
    # --- QOL Methods ---
    def get_user_by_email(self, email: str) -> Optional[User]:
        filters = [("email", "==", email.strip().lower())]  # Ensure email is case-insensitive
        user_dicts = self._db._query_collection(self._collection, filters)
        if user_dicts:
            return User(**user_dicts[0])  # Return the first matching user
        return None

users_manager = UsersManager()  # Singleton instance for easy access