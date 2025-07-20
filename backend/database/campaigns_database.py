from typing import Optional, List
from backend.database._database_core import database_manager
from backend.database.worlds_database import worlds_manager
from backend.models import Campaign, World

class CampaignsManager:
    """
    A class for managing campaign data in a Firestore database.
    """
    def __init__(self):
        self._db = database_manager
        self._collection = "campaigns"
    
    # === Core CRUD Operations ===
    def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        data = self._db._get_document(self._collection, campaign_id)
        if data:
            return Campaign(**data)
        return None

    def add_campaign(self, campaign: Campaign) -> Optional[str]:
        return self._db._add_document(self._collection, campaign.model_dump())

    def update_campaign(self, campaign: Campaign) -> bool:
        return self._db._update_document(self._collection, campaign.id, campaign.model_dump(exclude_unset=True))

    def delete_campaign(self, campaign_id: str) -> bool:
        return self._db._delete_document(self._collection, campaign_id)

    def get_all_campaigns(self, limit: Optional[int] = None) -> List[Campaign]:
        campaign_dicts = self._db._list_documents(self._collection, limit)
        return [Campaign(**data) for data in campaign_dicts if data]

    def query_campaigns(self, filters: List[tuple], limit: Optional[int] = None) -> List[Campaign]:
        campaign_dicts = self._db._query_collection(self._collection, filters, limit)
        return [Campaign(**data) for data in campaign_dicts if data]
    
    # === Helper Methods ===
    def get_campaigns_by_user(self, user_id: str) -> List[Campaign]:
        filters = [("creator_id", "==", user_id)]
        campaign_dicts = self._db._query_collection(self._collection, filters)
        return [Campaign(**data) for data in campaign_dicts if data]
    
    def get_campaigns_by_world(self, world_id: str) -> List[Campaign]:
        filters = [("world_id", "==", world_id)]
        campaign_dicts = self._db._query_collection(self._collection, filters)
        return [Campaign(**data) for data in campaign_dicts if data]
    
    def from_world(self, world: World, creator_id: str) -> Campaign:
        """
        Create a new campaign from a world.
        This is useful for initializing a campaign based on an existing world.
        """
        
        new_campaign = Campaign(
            world_id=world.id,
            name=f"Campaign for {world.name}",
            description=f"Campaign in {world.name}. Created by {creator_id}.",
            creator_id=creator_id,
            context=world.context,
            settings=world.settings,
            members={creator_id: "Creator"},
            turn_queue=[],
            is_public=world.is_public,
            era_ids=[],
        )
        self.add_campaign(new_campaign)
        return new_campaign
    
    def sync_with_world(self, campaign_id: str) -> None:
        """
        Sync campaigns with the world context and settings.
        This can be used to update campaigns when a world is modified.
        """
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            return
        
        if not campaign.world_id:
            return
        
        world = worlds_manager.get_world(campaign.world_id)
        if not world:
            return
        
        # Merge update campaign context and settings from the world
        campaign.context = world.context
        campaign.settings = world.settings
        self.update_campaign(campaign)
    
    def to_world(self, campaign: Campaign) -> World:
        """
        Convert a Campaign to a World.
        This is useful for creating a world from an existing campaign.
        """
        
        return World(
            name=f"{campaign.name} - World",
            description=campaign.description,
            creator_id=campaign.creator_id,
            is_public=campaign.is_public,
            context=campaign.context,
            settings=campaign.settings
        )

campaigns_manager = CampaignsManager()
