import uuid
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from enum import Enum

# === === Utility === ===
def generate_id(prefix: str = "") -> str:
    return f"{prefix}_{str(uuid.uuid4())[:8]}"

# === === Base === ===
class BaseDocument(BaseModel):
    id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def diff(self, other: 'BaseDocument') -> dict[str, tuple[Any, Any]]:
        if not isinstance(other, type(self)):
            raise ValueError(f"Cannot diff {type(self)} with {type(other)}")

        changes = {}
        for field in type(self).model_fields:
            old_val = getattr(self, field)
            new_val = getattr(other, field)
            if old_val != new_val:
                changes[field] = (old_val, new_val)
        return changes

# === === Identification Models === ===
class User(BaseDocument):
    id: str = Field(default_factory=lambda: generate_id("USR"))
    email: EmailStr
    username: str
    password_hashed: str
    member_ids: List[str] = Field(default_factory=list) # IDs of Member documents
    world_ids: List[str] = Field(default_factory=list) # IDs of World documents
    campaign_ids: List[str] = Field(default_factory=list) # IDs of Campaign documents

    def get_members(self) -> List['Member']:
        from backend.database.repos import member_repo
        members = []
        for id in self.member_ids:
            member = member_repo.get(id)
            if member is not None:
                members.append(member)
        return members
    
    def get_worlds(self) -> List['World']:
        from backend.database.repos import world_repo
        worlds = []
        for wid in self.world_ids:
            world = world_repo.get(wid)
            if world is not None:
                worlds.append(world)
        return worlds

    def get_campaigns(self) -> List['Campaign']:
        from backend.database.repos import campaign_repo
        campaigns = []
        for cid in self.campaign_ids:
            campaign = campaign_repo.get(cid)
            if campaign is not None:
                campaigns.append(campaign)
        return campaigns        

    def delete(self, batch):
        from backend.database import fs, REPO

        if REPO.USERS.get(self.id) is None:
            raise ValueError("User does not exist in repository.")

        _batch = batch if batch else fs.create_batch()

        members = self.get_members()
        for member in members:
            member.is_active = False
            member.user_id = None
            REPO.MEMBERS.batch_update(_batch, member)

        REPO.USERS.batch_delete(_batch, self.id)

        return _batch

class Member(BaseDocument):
    id: str = Field(default_factory=lambda: generate_id("MBR"))
    user_id: Optional[str] = None # ID of the associated User document; No user_id + is_active means AI Controlled member
    campaign_id: str # ID of the Campaign document
    is_admin: bool = False
    is_dm: bool = False
    is_active: bool = False
    character_id: Optional[str] = None # ID of the Character Object document
    equipped_ids: List[str] = Field(default_factory=list) # IDs of Object documents in inventory that are equipped
    inventory_ids: List[str] = Field(default_factory=list) # IDs of Object documents in inventory (not equipped)

    def get_user(self) -> Optional[User]:
        from backend.database.repos import user_repo
        if self.user_id:
            return user_repo.get(self.user_id)
        return None
    
    def get_campaign(self) -> Optional['Campaign']:
        from backend.database.repos import campaign_repo
        return campaign_repo.get(self.campaign_id)

    def get_character(self) -> Optional['Object']:
        from backend.database.repos import object_repo
        if self.character_id:
            return object_repo.get(self.character_id)
        return None
    
    def get_equipped(self) -> List['Object']:
        from backend.database.repos import object_repo
        equipped = []
        for oid in self.equipped_ids:
            obj = object_repo.get(oid)
            if obj is not None:
                equipped.append(obj)
        return equipped
    
    def get_inventory(self) -> List['Object']:
        from backend.database.repos import object_repo
        inventory = []
        for oid in self.inventory_ids:
            obj = object_repo.get(oid)
            if obj is not None:
                inventory.append(obj)
        return inventory
    
    def delete(self, batch):
        from backend.database import fs, REPO

        if REPO.MEMBERS.get(self.id) is None:
            raise ValueError("Member does not exist in repository.")

        _batch = batch if batch else fs.create_batch()

        user = self.get_user()
        if user is not None:
            user.member_ids.remove(self.id)
            REPO.USERS.batch_update(_batch, user)

        campaign = self.get_campaign()
        if campaign is not None:
            campaign.member_ids.remove(self.id)
            REPO.CAMPAIGNS.batch_update(_batch, campaign)

        REPO.MEMBERS.batch_delete(_batch, self.id)

        return _batch

# === === Game Setting Models === ===
class World(BaseDocument):
    id: str = Field(default_factory=lambda: generate_id("WRL"))
    name: str
    description: Optional[str] = None
    settings: Dict[str, Any] = Field(default_factory=dict)
    blueprint_ids: List[str] = Field(default_factory=list) # IDs of blueprint Object documents
    object_ids: List[str] = Field(default_factory=list) # IDs of Object documents
    context_ids: List[str] = Field(default_factory=list) # IDs of Context documents

    def get_blueprints(self) -> List['Blueprint']:
        from backend.database.repos import blueprint_repo
        blueprints = []
        for bid in self.blueprint_ids:
            blueprint = blueprint_repo.get(bid)
            if blueprint is not None:
                blueprints.append(blueprint)
        return blueprints

    def get_objects(self) -> List['Object']:
        from backend.database.repos import object_repo
        objects = []
        for oid in self.object_ids:
            obj = object_repo.get(oid)
            if obj is not None:
                objects.append(obj)
        return objects

    def get_contexts(self) -> List['Context']:
        from backend.database.repos import context_repo
        contexts = []
        for cid in self.context_ids:
            context = context_repo.get(cid)
            if context is not None:
                contexts.append(context)
        return contexts
    
    def delete(self, batch):
        from backend.database import fs, REPO

        if REPO.WORLDS.get(self.id) is None:
            raise ValueError("World does not exist in repository.")

        _batch = batch if batch else fs.create_batch()

        blueprints = self.get_blueprints()
        for blueprint in blueprints:
            REPO.BLUEPRINTS.batch_delete(_batch, blueprint.id)

        objects = self.get_objects()
        for obj in objects:
            REPO.OBJECTS.batch_delete(_batch, obj.id)

        contexts = self.get_contexts()
        for context in contexts:
            REPO.CONTEXTS.batch_delete(_batch, context.id)

        REPO.WORLDS.batch_delete(_batch, self.id)

        return _batch
    
    def to_campaign(self) -> 'Campaign':
        return Campaign(
            world_id=self.id,
            name=f"Campaign in {self.name}",
            description=self.description,
            settings=self.settings.copy(),
            member_ids=[],
            blueprint_ids=self.blueprint_ids.copy(),
            object_ids=self.object_ids.copy(),
            context_ids=self.context_ids.copy(),
            quest_ids=[]
        )

class Campaign(BaseDocument):
    id: str = Field(default_factory=lambda: generate_id("CMP"))
    world_id: Optional[str] = None  # ID of the World document
    name: str
    description: Optional[str] = None
    settings: Dict[str, Any] = Field(default_factory=dict)
    member_ids: List[str] = Field(default_factory=list)  # IDs of Member documents
    blueprint_ids: List[str] = Field(default_factory=list)  # IDs of blueprint Object documents
    object_ids: List[str] = Field(default_factory=list)  # IDs of Object documents
    context_ids: List[str] = Field(default_factory=list)  # IDs of Context documents
    quest_ids: List[str] = Field(default_factory=list)  # IDs of Quest documents

    def get_world(self) -> Optional[World]:
        from backend.database.repos import world_repo
        if self.world_id:
            return world_repo.get(self.world_id)
        return None

    def get_members(self) -> List['Member']:
        from backend.database.repos import member_repo
        members = []
        for mid in self.member_ids:
            member = member_repo.get(mid)
            if member is not None:
                members.append(member)
        return members
    
    def get_blueprints(self) -> List['Blueprint']:
        from backend.database.repos import blueprint_repo
        blueprints = []
        for bid in self.blueprint_ids:
            blueprint = blueprint_repo.get(bid)
            if blueprint is not None:
                blueprints.append(blueprint)
        return blueprints
    
    def get_objects(self) -> List['Object']:
        from backend.database.repos import object_repo
        objects = []
        for oid in self.object_ids:
            obj = object_repo.get(oid)
            if obj is not None:
                objects.append(obj)
        return objects
    
    def get_contexts(self) -> List['Context']:
        from backend.database.repos import context_repo
        contexts = []
        for cid in self.context_ids:
            context = context_repo.get(cid)
            if context is not None:
                contexts.append(context)
        return contexts

    def get_quests(self) -> List['Quest']:
        from backend.database.repos import quest_repo
        quests = []
        for qid in self.quest_ids:
            quest = quest_repo.get(qid)
            if quest is not None:
                quests.append(quest)
        return quests

    def delete(self, batch):
        from backend.database import fs, REPO

        if REPO.CAMPAIGNS.get(self.id) is None:
            raise ValueError("Campaign does not exist in repository.")

        _batch = batch if batch else fs.create_batch()

        members = self.get_members()
        for member in members:
            user = member.get_user()
            if user is not None:
                user.member_ids.remove(member.id)
                REPO.USERS.batch_update(_batch, user)

            REPO.MEMBERS.batch_delete(_batch, member.id)

        blueprints = self.get_blueprints()
        for blueprint in blueprints:
            REPO.BLUEPRINTS.batch_delete(_batch, blueprint.id)

        objects = self.get_objects()
        for obj in objects:
            REPO.OBJECTS.batch_delete(_batch, obj.id)

        contexts = self.get_contexts()
        for context in contexts:
            REPO.CONTEXTS.batch_delete(_batch, context.id)

        quests = self.get_quests()
        for quest in quests:
            REPO.QUESTS.batch_delete(_batch, quest.id)

        REPO.CAMPAIGNS.batch_delete(_batch, self.id)

        return _batch

# === === Content Models === ===
class AttributeType(str, Enum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    OBJECT = "object"

class Attribute(BaseModel):
    name: str
    type: AttributeType
    values: List[Any] = Field(default_factory=list)
    options: Optional[List[Any]] = None
    is_required: bool = False
    is_list: bool = False
    is_dropdown: bool = False
    attribute_binding: Optional[str] = None

class BlueprintBinding(str, Enum):
    PLAYER_CHARACTER = "pc" # Player Character
    NON_PLAYER_CHARACTER = "npc" # Non-Player Character
    RACE = "race" # Species / Race
    ANIMAL = "animal" # Animals / Creatures
    FACTION = "faction" # Faction / Organization / Tribe / Kingdom / Squad
    WEAPON = "weapon" # Weapon
    ABILITY = "ability" # Ability / Skill / Power
    ARMOR = "armor" # Armor / Shield
    ACCESSORY = "accessory" # Accessory / Clothing / Mask
    TOOL = "tool" # Tool / Gadget
    CURRENCY = "currency" # Currency
    CONSUMABLE = "consumable" # Consumable / Potion / Food / Ammunition
    ITEM = "item" # Item / Miscellaneous
    STATUS = "status" # Status on Player/Non-Player Character
    CONDITION = "condition" # Conditions in Environment
    LOCATION = "location" # Location / Building / Area
    VEHICLE = "vehicle" # Vehicle / Mount

class Blueprint(BaseDocument):
    id: str = Field(default_factory=lambda: generate_id("BLP"))
    name: str
    description: Optional[str] = None
    blueprint_binding: Optional[BlueprintBinding] = None
    attributes: List[Attribute] = Field(default_factory=list)

    def get_attribute(self, name: str) -> Optional[Attribute]:
        for attr in self.attributes:
            if attr.name == name:
                return attr
        return None
    
    def get_owner(self) -> Optional[World | Campaign]:
        from backend.database.repos import world_repo, campaign_repo
        if len(worlds := world_repo.query([("blueprint_ids", "array_contains", self.id)])) > 0:
            return worlds[0]
        
        if len(campaigns := campaign_repo.query([("blueprint_ids", "array_contains", self.id)])) > 0:
            return campaigns[0]
        return None
    
    def get_objects(self) -> List['Object']:
        from backend.database.repos import object_repo
        objects = []
        for obj in object_repo.query([("blueprint_id", "==", self.id)]):
            objects.append(obj)
        return objects

    def to_object(self) -> 'Object':
        return Object(
            blueprint_id=self.id,
            name=f"New {self.name}",
            description=None,
            blueprint_binding=self.blueprint_binding,
            attributes=self.attributes.copy()
        )
    
    def delete(self, batch):
        from backend.database import fs, REPO

        if REPO.BLUEPRINTS.get(self.id) is None:
            raise ValueError("Blueprint does not exist in repository.")

        _batch = batch if batch else fs.create_batch()

        owner = self.get_owner()

        objects = self.get_objects()
        for obj in objects:
            REPO.OBJECTS.batch_delete(_batch, obj.id)
            if owner is not None:
                owner.object_ids.remove(obj.id)

        if owner is not None:
            owner.blueprint_ids.remove(self.id)
            if isinstance(owner, Campaign):
                REPO.CAMPAIGNS.batch_update(_batch, owner)
            elif isinstance(owner, World):
                REPO.WORLDS.batch_update(_batch, owner)

        REPO.BLUEPRINTS.batch_delete(_batch, self.id)

        return _batch

class Object(BaseDocument):
    id: str = Field(default_factory=lambda: generate_id("OBJ"))
    blueprint_id: str # ID of the associated Blueprint document
    name: str
    description: Optional[str] = None
    blueprint_binding: Optional[BlueprintBinding] = None
    attributes: List[Attribute] = Field(default_factory=list)

    def get_blueprint(self) -> Optional[Blueprint]:
        from backend.database.repos import blueprint_repo
        if self.blueprint_id:
            return blueprint_repo.get(self.blueprint_id)
        return None

    def get_attribute(self, name: str) -> Optional[Attribute]:
        for attr in self.attributes:
            if attr.name == name:
                return attr
        return None
    
    def get_owner(self) -> Optional[World | Campaign]:
        from backend.database.repos import world_repo, campaign_repo
        if len(worlds := world_repo.query([("object_ids", "array_contains", self.id)])) > 0:
            return worlds[0]
        
        if len(campaigns := campaign_repo.query([("object_ids", "array_contains", self.id)])) > 0:
            return campaigns[0]
        return None
    
    def normalize(self) -> bool:
        blueprint = self.get_blueprint()
        if blueprint is None:
            return False

        import copy
        obj_attr_map = {attr.name: attr for attr in self.attributes}
        normalized_attrs = []

        for blp_attr in blueprint.attributes:
            obj_attr = obj_attr_map.get(blp_attr.name)
            if obj_attr:
                normalized_attrs.append(obj_attr)
            else:
                if blp_attr.is_required:
                    normalized_attrs.append(copy.deepcopy(blp_attr))

        self.blueprint_binding = blueprint.blueprint_binding
        self.attributes = normalized_attrs

        return True
    
    def delete(self, batch):
        from backend.database import fs, REPO

        if REPO.OBJECTS.get(self.id) is None:
            raise ValueError("Object does not exist in repository.")

        _batch = batch if batch else fs.create_batch()

        owner = self.get_owner()
        if owner is not None:
            owner.object_ids.remove(self.id)
            if isinstance(owner, Campaign):
                REPO.CAMPAIGNS.batch_update(_batch, owner)
            elif isinstance(owner, World):
                REPO.WORLDS.batch_update(_batch, owner)

        REPO.OBJECTS.batch_delete(_batch, self.id)

        return _batch

class Context(BaseDocument):
    id: str = Field(default_factory=lambda: generate_id("CTX"))
    name: str
    content: str

    def get_owner(self) -> Optional[World | Campaign]:
        from backend.database.repos import world_repo, campaign_repo
        if len(worlds := world_repo.query([("context_ids", "array_contains", self.id)])) > 0:
            return worlds[0]

        if len(campaigns := campaign_repo.query([("context_ids", "array_contains", self.id)])) > 0:
            return campaigns[0]
        return None
    
    def delete(self, batch):
        from backend.database import fs, REPO

        if REPO.CONTEXTS.get(self.id) is None:
            raise ValueError("Context does not exist in repository.")

        _batch = batch if batch else fs.create_batch()

        owner = self.get_owner()
        if owner is not None:
            owner.context_ids.remove(self.id)
            if isinstance(owner, Campaign):
                REPO.CAMPAIGNS.batch_update(_batch, owner)
            elif isinstance(owner, World):
                REPO.WORLDS.batch_update(_batch, owner)

        REPO.CONTEXTS.batch_delete(_batch, self.id)

        return _batch

class Quest(BaseDocument):
    id: str = Field(default_factory=lambda: generate_id("QST"))
    name: str
    description: Optional[str] = None
    task: str
    is_main: bool = False
    is_active: bool = False
    is_complete: bool = False
    parent_id: Optional[str] = None # ID of parent quest
    children_ids: List[str] = Field(default_factory=list) # IDs of sub-quests

    def get_parent(self) -> Optional['Quest']:
        from backend.database.repos import quest_repo
        if self.parent_id:
            return quest_repo.get(self.parent_id)
        return None

    def get_children(self) -> List['Quest']:
        from backend.database.repos import quest_repo
        children = []
        for cid in self.children_ids:
            child = quest_repo.get(cid)
            if child is not None:
                children.append(child)
        return children
    
    def get_progress(self) -> float:
        children = self.get_children()
        if len(children) == 0:
            return 1.0 if self.is_complete else 0.0
        
        completed = sum(child.get_progress() for child in children)

        return completed / len(children)
    
    def get_owner(self) -> Optional[Campaign]:
        from backend.database.repos import campaign_repo
        if len(campaigns := campaign_repo.query([("quest_ids", "array_contains", self.id)])) > 0:
            return campaigns[0]
        return None
    
    def delete(self, batch):
        from backend.database import fs, REPO

        if REPO.QUESTS.get(self.id) is None:
            raise ValueError("Quest does not exist.")

        if self.parent_id is not None:
            raise ValueError("Only root quests may be deleted.")

        _batch = batch if batch else fs.create_batch()

        owner = self.get_owner()
        if owner and self.id in owner.quest_ids:
            owner.quest_ids.remove(self.id)
            REPO.CAMPAIGNS.batch_update(_batch, owner)

        self._delete_subtree(_batch)

        return _batch

    
    def _delete_subtree(self, batch):
        from backend.database import REPO

        for child in self.get_children():
            child._delete_subtree(batch)

        REPO.QUESTS.batch_delete(batch, self.id)

# === === Timeline Models === ===
class ActionType(str, Enum):
    # Skip
    WAIT = "wait"

    # Combat
    ATTACK = "attack"
    DEFEND = "defend"
    DODGE = "dodge"

    # Move
    MOVE = "move"
    ADV_MOVE = "adv_move"
    SNEAK = "sneak"

    # Social
    PERSUADE = "persuade"
    INTIMIDATE = "intimidate"
    ANTAGONIZE = "antagonize"
    DECEIVE = "deceive"

    # Usage
    ACTIVATE = "activate"       # using items/tools
    USE_ITEM = "use_item"       # using consumables
    CAST = "cast"               # using abilities/spells/powers
    INTERACT = "interact"       # interacting with NPCs/environment
    INVESTIGATE = "investigate" # find clues, secrets, traps, ...

    # Misc
    SIMPLE = "simple"           # uncategorized - straightforward action, valid
    IMPOSSIBLE = "impossible"   # uncategorized - impossible action, invalid

class ActionStatus(str, Enum):
    WAITING = "waiting"
    ROLLING = "rolling"
    DENIED = "denied"
    CRIT_FAILURE = "crit_failure"
    FAILURE = "failure"
    SUCCESS = "success"
    CRIT_SUCCESS = "crit_success"

class Action(BaseModel):
    member_id: str # ID of the member performing the action
    type: Optional[ActionType] = None
    intent: str
    status: ActionStatus = ActionStatus.WAITING 
    item_ids: List[str] = Field(default_factory=list) # IDs of Object documents used for this action
    target_ids: List[str] = Field(default_factory=list) # IDs of Object documents targeted
    requirement: Optional[int] = None # e.g., (0-100) roll needed to succeed; None if automatic success

    def get_member(self) -> Optional[Member]:
        from backend.database.repos import member_repo
        return member_repo.get(self.member_id)
    
    def get_items(self) -> List[Object]:
        from backend.database.repos import object_repo
        items = []
        for oid in self.item_ids:
            obj = object_repo.get(oid)
            if obj is not None:
                items.append(obj)
        return items

    def get_targets(self) -> List[Object]:
        from backend.database.repos import object_repo
        targets = []
        for oid in self.target_ids:
            obj = object_repo.get(oid)
            if obj is not None:
                targets.append(obj)
        return targets

class Scene(BaseDocument):
    id: str = Field(default_factory=lambda: generate_id("SCN"))
    campaign_id: str # ID of the campaign this scene belongs to
    encounter_id: str # ID of the encounter this scene belongs to
    content: str
    summary: Optional[str] = None
    actions: List[Action] = Field(default_factory=list)
    minute_time: int # In-game minute (0-1440) timestamp of the scene

    def get_campaign(self) -> Optional[Campaign]:
        from backend.database.repos import campaign_repo
        return campaign_repo.get(self.campaign_id)
    
    def get_encounter(self) -> Optional['Encounter']:
        from backend.database.repos import encounter_repo
        return encounter_repo.get(self.encounter_id)
    
    def get_time(self) -> str:
        hours = self.minute_time // 60
        minutes = self.minute_time % 60
        if hours >= 24:
            hours = hours % 24

        if hours == 0:
            hours = 12
            period = "AM"
        elif hours < 12:
            period = "AM"
        else:
            period = "PM"
        
        return f"{hours:02}:{minutes:02} {period}"
    
    def delete(self, batch):
        from backend.database import fs, REPO

        if REPO.SCENES.get(self.id) is None:
            raise ValueError("Scene does not exist in repository.")

        _batch = batch if batch else fs.create_batch()

        encounter = self.get_encounter()
        if encounter and self.id in encounter.scene_ids:
            encounter.scene_ids.remove(self.id)
            REPO.ENCOUNTERS.batch_update(_batch, encounter)

        REPO.SCENES.batch_delete(_batch, self.id)

        return _batch

class EncounterType(str, Enum):
    COMBAT = "combat"
    EXPLORATION = "exploration"
    SOCIAL = "social"
    PUZZLE = "puzzle"
    STORE = "store"
    TRAVEL = "travel"
    MISC = "miscellaneous"

class Encounter(BaseDocument):
    id: str = Field(default_factory=lambda: generate_id("ENC"))
    campaign_id: str # ID of the campaign this encounter belongs to
    chapter_id: str # ID of the chapter this encounter belongs to
    type: str
    goal: str
    length: int
    scene_ids: List[str] = Field(default_factory=list) # IDs of scenes in this encounter
    
    def get_campaign(self) -> Optional[Campaign]:
        from backend.database.repos import campaign_repo
        return campaign_repo.get(self.campaign_id)
    
    def get_chapter(self) -> Optional['Chapter']:
        from backend.database.repos import chapter_repo
        return chapter_repo.get(self.chapter_id)

    def get_scenes(self, limit: int = -1) -> List['Scene']:
        from backend.database.repos import scene_repo
        scenes = []
        if limit == -1:
            limit = len(self.scene_ids)
        for sid in self.scene_ids[:limit]:
            scene = scene_repo.get(sid)
            if scene is not None:
                scenes.append(scene)
        return scenes
    
    def get_progress(self) -> float:
        if self.length == 0:
            return 0.0
        return min(len(self.scene_ids) / self.length, 1.0)
    
    def delete(self, batch):
        from backend.database import fs, REPO

        if REPO.ENCOUNTERS.get(self.id) is None:
            raise ValueError("Encounter does not exist in repository.")

        _batch = batch if batch else fs.create_batch()

        chapter = self.get_chapter()
        if chapter and self.id in chapter.encounter_ids:
            chapter.encounter_ids.remove(self.id)
            REPO.CHAPTERS.batch_update(_batch, chapter)

        scenes = self.get_scenes()
        for scene in scenes:
            REPO.SCENES.batch_delete(_batch, scene.id)

        REPO.ENCOUNTERS.batch_delete(_batch, self.id)

        return _batch

class Chapter(BaseDocument):
    id: str = Field(default_factory=lambda: generate_id("CHP"))
    campaign_id: str # ID of the campaign this chapter belongs to
    description: Optional[str] = None
    encounter_ids: List[str] = Field(default_factory=list) # IDs of encounters in this chapter

    def get_campaign(self) -> Optional[Campaign]:
        from backend.database.repos import campaign_repo
        return campaign_repo.get(self.campaign_id)
    
    def get_encounters(self, limit: int = -1) -> List['Encounter']:
        from backend.database.repos import encounter_repo
        encounters = []
        if limit == -1:
            limit = len(self.encounter_ids)
        for eid in self.encounter_ids[:limit]:
            encounter = encounter_repo.get(eid)
            if encounter is not None:
                encounters.append(encounter)
        return encounters

    def get_scenes(self, limit: int = -1) -> List['Scene']:
        scenes = []
        encounters = self.get_encounters()
        for encounter in encounters:
            scenes.extend(encounter.get_scenes(limit))
            if limit != -1 and len(scenes) >= limit:
                return scenes[:limit]
        return scenes[:limit] if limit != -1 else scenes
    
    def delete(self, batch):
        from backend.database import fs, REPO

        if REPO.CHAPTERS.get(self.id) is None:
            raise ValueError("Chapter does not exist in repository.")

        _batch = batch if batch else fs.create_batch()

        encounters = self.get_encounters()
        for encounter in encounters:
            REPO.ENCOUNTERS.batch_delete(_batch, encounter.id)
            scenes = encounter.get_scenes()
            for scene in scenes:
                REPO.SCENES.batch_delete(_batch, scene.id)

        REPO.CHAPTERS.batch_delete(_batch, self.id)

        return _batch

User.model_rebuild()
Member.model_rebuild()
World.model_rebuild()
Campaign.model_rebuild()
Blueprint.model_rebuild()
Object.model_rebuild()
Context.model_rebuild()
Quest.model_rebuild()
Action.model_rebuild()
Scene.model_rebuild()
Encounter.model_rebuild()
Chapter.model_rebuild()
