from typing import Optional, List
from backend.database._database_core import database_manager
from backend.models import World

class WorldsManager:
    """
    A class for managing world data in a Firestore database.
    """

    def __init__(self):
        self._db = database_manager
        self._collection = "worlds"
    
    # === Core CRUD Operations ===
    def get_world(self, world_id: str) -> Optional[World]:
        data = self._db._get_document(self._collection, world_id)
        if data:
            return World(**data)
        return None

    def add_world(self, world: World) -> Optional[str]:
        return self._db._add_document(self._collection, world.model_dump())

    def update_world(self, world: World) -> bool:
        return self._db._update_document(self._collection, world.id, world.model_dump(exclude_unset=True))

    def delete_world(self, world_id: str) -> bool:
        return self._db._delete_document(self._collection, world_id)

    def get_all_worlds(self, limit: Optional[int] = None) -> List[World]:
        world_dicts = self._db._list_documents(self._collection, limit)
        return [World(**data) for data in world_dicts if data]

    def query_worlds(self, filters: List[tuple], limit: Optional[int] = None) -> List[World]:
        world_dicts = self._db._query_collection(self._collection, filters, limit)
        return [World(**data) for data in world_dicts if data]

    # === Helper Methods ===
    def get_worlds_by_user(self, user_id: str) -> List[World]:
        filters = [("creator_id", "==", user_id)]
        world_dicts = self._db._query_collection(self._collection, filters)
        return [World(**data) for data in world_dicts if data]

worlds_manager = WorldsManager()
