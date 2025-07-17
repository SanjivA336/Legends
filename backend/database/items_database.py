from typing import Optional, List
from backend.database._database_core import database_manager
from backend.models import Item

class ItemsManager:
    """
    A class for managing item data in a Firestore database.
    """
    def __init__(self):
        self._db = database_manager
        self._collection = "items"
    
    # --- Core CRUD Operations ---
    def get_item(self, item_id: str) -> Optional[Item]:
        data = self._db._get_document(self._collection, item_id)
        if data:
            return Item(**data)
        return None

    def add_item(self, item: Item) -> Optional[str]:
        return self._db._add_document(self._collection, item.model_dump())

    def update_item(self, item: Item) -> bool:
        return self._db._update_document(self._collection, item.id, item.model_dump(exclude_unset=True))

    def delete_item(self, item_id: str) -> bool:
        return self._db._delete_document(self._collection, item_id)

    def get_all_items(self, limit: Optional[int] = None) -> List[Item]:
        item_dicts = self._db._list_documents(self._collection, limit)
        return [Item(**data) for data in item_dicts if data]

    def query_items(self, filters: List[tuple], limit: Optional[int] = None) -> List[Item]:
        item_dicts = self._db._query_collection(self._collection, filters, limit)
        return [Item(**data) for data in item_dicts if data]

items_manager = ItemsManager()
