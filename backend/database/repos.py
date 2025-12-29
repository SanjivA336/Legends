# database/base_repo.py
from typing import TypeVar, Generic, Type, List, Optional, Dict, Any
from backend.models.models import BaseDocument
from backend.database import fs
from google.cloud import firestore

from datetime import datetime, timezone
from uuid import uuid4

T = TypeVar("T", bound=BaseDocument)

class BaseRepo(Generic[T]):
    def __init__(self, model_cls: Type[T], collection: str):
        self._db = fs
        self._collection = collection
        self._model_cls = model_cls

    def get(self, id: str) -> Optional[T]:
        return self._db.get_document(self._collection, id, self._model_cls)

    def add(self, obj: T) -> Optional[T]:
        if self._db.add_document(self._collection, obj):
            return self.get(obj.id)
        return None

    def update(self, obj: T) -> Optional[T]:
        if self._db.update_document(self._collection, obj.id, obj.model_dump(exclude_unset=True)):
            return self.get(obj.id)
        return None

    def delete(self, id: str) -> bool:
        self._db.delete_document(self._collection, id)
        return self.get(id) is None

    def list(self, limit: Optional[int] = None) -> List[T]:
        return self._db.list_documents(self._collection, self._model_cls, limit)

    def query(self, filters: List[tuple], limit: Optional[int] = None) -> List[T]:
        return self._db.query_collection(self._collection, filters, self._model_cls, limit)
    
    def batch_add(self, batch: firestore.WriteBatch, obj: T):
        doc_ref = self._db._db.collection(self._collection).document(obj.id)
        batch.set(doc_ref, obj.model_dump())

    def batch_update(self, batch: firestore.WriteBatch, obj: T):
        doc_ref = self._db._db.collection(self._collection).document(obj.id)
        batch.update(doc_ref, obj.model_dump(exclude_unset=True))
    
    def batch_delete(self, batch: firestore.WriteBatch, doc_id: str):
        doc_ref = self._db._db.collection(self._collection).document(doc_id)
        batch.delete(doc_ref)
    
from backend.models.models import (
    User, Member, World, Campaign, Blueprint, Object, Context, Quest, Scene, Encounter, Chapter
)

user_repo = BaseRepo[User](User, "users")
member_repo = BaseRepo[Member](Member, "members")
world_repo = BaseRepo[World](World, "worlds")
campaign_repo = BaseRepo[Campaign](Campaign, "campaigns")
blueprint_repo = BaseRepo[Blueprint](Blueprint, "blueprints")
object_repo = BaseRepo[Object](Object, "objects")
context_repo = BaseRepo[Context](Context, "contexts")
quest_repo = BaseRepo[Quest](Quest, "quests")
scene_repo = BaseRepo[Scene](Scene, "scenes")
encounter_repo = BaseRepo[Encounter](Encounter, "encounters")
chapter_repo = BaseRepo[Chapter](Chapter, "chapters")

class RepoContainer:
    USERS = user_repo
    MEMBERS = member_repo
    WORLDS = world_repo
    CAMPAIGNS = campaign_repo
    BLUEPRINTS = blueprint_repo
    OBJECTS = object_repo
    CONTEXTS = context_repo
    QUESTS = quest_repo
    SCENES = scene_repo
    ENCOUNTERS = encounter_repo
    CHAPTERS = chapter_repo

REPO = RepoContainer()