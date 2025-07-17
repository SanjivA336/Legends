from typing import Optional, List
from backend.database._database_core import database_manager
from backend.models import Actor

class ActorsManager:
    """
    A class for managing actor data in a Firestore database.
    """
    def __init__(self):
        self._db = database_manager
        self._collection = "actors"
    
    # --- Core CRUD Operations ---
    def get_actor(self, actor_id: str) -> Optional[Actor]:
        data = self._db._get_document(self._collection, actor_id)
        if data:
            return Actor(**data)
        return None

    def add_actor(self, actor: Actor) -> Optional[str]:
        return self._db._add_document(self._collection, actor.model_dump())

    def update_actor(self, actor: Actor) -> bool:
        return self._db._update_document(self._collection, actor.id, actor.model_dump(exclude_unset=True))

    def delete_actor(self, actor_id: str) -> bool:
        return self._db._delete_document(self._collection, actor_id)

    def get_all_actors(self, limit: Optional[int] = None) -> List[Actor]:
        actor_dicts = self._db._list_documents(self._collection, limit)
        return [Actor(**data) for data in actor_dicts if data]

    def query_actors(self, filters: List[tuple], limit: Optional[int] = None) -> List[Actor]:
        actor_dicts = self._db._query_collection(self._collection, filters, limit)
        return [Actor(**data) for data in actor_dicts if data]

actors_manager = ActorsManager()
