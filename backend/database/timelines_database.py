from typing import Optional, List
from backend.database._database_core import database_manager
from backend.models import TimelineNode

class TimelineNodesManager:
    """
    A class for managing timeline node data in a Firestore database.
    """
    def __init__(self):
        self._db = database_manager
        self._collection = "timeline_nodes"
    
    # --- Core CRUD Operations ---
    def get_timeline_node(self, node_id: str) -> Optional[TimelineNode]:
        data = self._db._get_document(self._collection, node_id)
        if data:
            return TimelineNode(**data)
        return None

    def add_timeline_node(self, node: TimelineNode) -> Optional[str]:
        return self._db._add_document(self._collection, node.model_dump())

    def update_timeline_node(self, node: TimelineNode) -> bool:
        return self._db._update_document(self._collection, node.id, node.model_dump(exclude_unset=True))

    def delete_timeline_node(self, node_id: str) -> bool:
        return self._db._delete_document(self._collection, node_id)

    def get_all_timeline_nodes(self, limit: Optional[int] = None) -> List[TimelineNode]:
        node_dicts = self._db._list_documents(self._collection, limit)
        return [TimelineNode(**data) for data in node_dicts if data]

    def query_timeline_nodes(self, filters: List[tuple], limit: Optional[int] = None) -> List[TimelineNode]:
        node_dicts = self._db._query_collection(self._collection, filters, limit)
        return [TimelineNode(**data) for data in node_dicts if data]

timelines_manager = TimelineNodesManager()
