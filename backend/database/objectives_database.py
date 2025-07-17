from typing import Optional, List
from backend.database._database_core import database_manager
from backend.models import Objective

class ObjectivesManager:
    """
    A class for managing objective data in a Firestore database.
    """
    def __init__(self):
        self._db = database_manager
        self._collection = "objectives"
    
    # --- Core CRUD Operations ---
    def get_objective(self, objective_id: str) -> Optional[Objective]:
        data = self._db._get_document(self._collection, objective_id)
        if data:
            return Objective(**data)
        return None

    def add_objective(self, objective: Objective) -> Optional[str]:
        return self._db._add_document(self._collection, objective.model_dump())

    def update_objective(self, objective: Objective) -> bool:
        return self._db._update_document(self._collection, objective.id, objective.model_dump(exclude_unset=True))

    def delete_objective(self, objective_id: str) -> bool:
        return self._db._delete_document(self._collection, objective_id)

    def get_all_objectives(self, limit: Optional[int] = None) -> List[Objective]:
        obj_dicts = self._db._list_documents(self._collection, limit)
        return [Objective(**data) for data in obj_dicts if data]

    def query_objectives(self, filters: List[tuple], limit: Optional[int] = None) -> List[Objective]:
        obj_dicts = self._db._query_collection(self._collection, filters, limit)
        return [Objective(**data) for data in obj_dicts if data]

objectives_manager = ObjectivesManager()
