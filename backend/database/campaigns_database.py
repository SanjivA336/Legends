from typing import Optional, List
from backend.database._database_core import database_manager
from backend.models import Campaign

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

campaigns_manager = CampaignsManager()
