# database/base_repo.py
from typing import TypeVar, Generic, Type, List, Optional, Dict, Any
from backend.models import BaseDocument
from backend.database.firestore_wrapper import firestore_wrapper

T = TypeVar("T", bound=BaseDocument)

class BaseRepo(Generic[T]):
    def __init__(self, model_cls: Type[T], collection: str):
        self._db = firestore_wrapper
        self._collection = collection
        self._model_cls = model_cls

    def get(self, id: str) -> Optional[T]:
        return self._db.get_document(self._collection, id, self._model_cls)

    def add(self, obj: T) -> Optional[str]:
        return self._db.add_document(self._collection, obj)

    def update(self, obj: T) -> bool:
        return self._db.update_document(self._collection, obj.id, obj.model_dump(exclude_unset=True))

    def delete(self, id: str) -> bool:
        return self._db.delete_document(self._collection, id)

    def list(self, limit: Optional[int] = None) -> List[T]:
        return self._db.list_documents(self._collection, self._model_cls, limit)

    def query(self, filters: List[tuple], limit: Optional[int] = None) -> List[T]:
        return self._db.query_collection(self._collection, filters, self._model_cls, limit)


from backend.models import (
    User, World, Campaign, Member, Context,
    Blueprint, Object, Era, Chapter, Encounter, Action,
    MinigameResult, Objective
)

users_repo = BaseRepo(User, "users")
worlds_repo = BaseRepo(World, "worlds")
campaigns_repo = BaseRepo(Campaign, "campaigns")
members_repo = BaseRepo(Member, "members")
context_repo = BaseRepo(Context, "context")
blueprints_repo = BaseRepo(Blueprint, "blueprints")
objects_repo = BaseRepo(Object, "objects")
objectives_repo = BaseRepo(Objective, "objectives")
eras_repo = BaseRepo(Era, "eras")
chapters_repo = BaseRepo(Chapter, "chapters")
encounters_repo = BaseRepo(Encounter, "encounters")
actions_repo = BaseRepo(Action, "actions")
minigames_repo = BaseRepo(MinigameResult, "minigames")
