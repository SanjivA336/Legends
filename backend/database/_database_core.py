import os
import json
from google.cloud import firestore
from google.oauth2 import service_account
from backend.models import User, Campaign, TimelineNode, Actor, Item, Objective
from typing import Optional, List, Dict, Any
import logging

# Wrapper class for Firestore operations
class DatabaseManager:
    """
    A wrapper class for Firestore operations with logging.
    Provides methods to add, get, update, delete, and query documents in Firestore collections.
    """

    def __init__(self):
        """
        Initializes the Firestore client and configures logging.
        """
        
        self._db = self._get_firestore_client()
        # Configure logging: INFO level logs to console with timestamps
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(name)s - %(message)s'
        )

        self._logger = logging.getLogger(__name__)  # Logger for this module

    def _get_firestore_client(self) -> firestore.Client:
        """
        Initializes and returns a Firestore client using credentials from environment variables or a file.
        Tries to load credentials from:
        1. Environment variable FIREBASE_CREDENTIALS containing JSON credentials.
        2. Environment variable FIREBASE_CREDENTIALS_PATH pointing to a service account JSON file.
        Raises RuntimeError if credentials cannot be loaded.
        """
        
        # 1. Try JSON credentials from environment variable
        creds_json = os.environ.get("FIREBASE_CREDENTIALS")
        if creds_json:
            try:
                service_account_info = json.loads(creds_json)
                credentials = service_account.Credentials.from_service_account_info(service_account_info)
                return firestore.Client(credentials=credentials, project=service_account_info.get("project_id"))
            except Exception as e:
                raise RuntimeError("Failed to load Firestore credentials from environment variable: " + str(e))

        # 2. Try file path from environment variable or default
        creds_path = os.environ.get("FIREBASE_CREDENTIALS_PATH", "backend/Keys/legends-firebase-serviceAccount.json")
        if os.path.exists(creds_path):
            try:
                credentials = service_account.Credentials.from_service_account_file(creds_path)
                return firestore.Client(credentials=credentials)
            except Exception as e:
                raise RuntimeError("Failed to load Firestore credentials from file: " + str(e))
            
        raise RuntimeError("No Firestore credentials found.")

    def _add_document(self, collection: str, data: Dict[str, Any]) -> Optional[str]:
        """
        Adds a new document to a collection. Fails if document already exists.
        
        """
        try:
            doc_id = data['id']
            self._db.collection(collection).document(doc_id).create(data)
            self._logger.info(f"Added document to {collection}/{doc_id}")
            return doc_id
        except Exception as e:
            self._logger.error(f"Error adding document to {collection}: {e}")
            return None

    def _get_document(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a document by ID from a collection.
        Returns the document data as a dict, or None if not found.
        """
        
        doc_ref = self._db.collection(collection).document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            self._logger.info(f"Retrieved document {collection}/{doc_id}")
            return doc.to_dict()
        else:
            self._logger.warning(f"Document {collection}/{doc_id} not found")
            return None

    def _update_document(self, collection: str, doc_id: str, updates: Dict[str, Any]) -> bool:
        """
        Updates specific fields (merge) in a document. Fails if document does not exist.
        """
        
        try:
            self._db.collection(collection).document(doc_id).update(updates)
            self._logger.info(f"Updated document {collection}/{doc_id} with fields {list(updates.keys())}")
            return True
        except Exception as e:
            self._logger.error(f"Error updating document {collection}/{doc_id}: {e}")
            return False

    def _delete_document(self, collection: str, doc_id: str) -> bool:
        """
        Deletes a document from a collection by ID.
        """
        
        try:
            self._db.collection(collection).document(doc_id).delete()
            self._logger.info(f"Deleted document {collection}/{doc_id}")
            return True
        except Exception as e:
            self._logger.error(f"Error deleting document {collection}/{doc_id}: {e}")
            return False

    def _query_collection(self, collection: str, filters: List[tuple], limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Queries a collection with a list of (field, op, value) filters.
        Returns a list of document dicts.
        """
        
        ref = self._db.collection(collection)
        query = ref
        for field, op, value in filters:
            query = query.where(field, op, value)
        if limit:
            query = query.limit(limit)
        try:
            results = query.stream()
            docs = [doc.to_dict() for doc in results]
            self._logger.info(f"Query on {collection} with filters {filters} returned {len(docs)} documents")
            return docs
        except Exception as e:
            self._logger.error(f"Error querying collection {collection} with filters {filters}: {e}")
            return []

    def _list_documents(self, collection: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Lists all documents in a collection. Can limit the number of results.
        """
        
        ref = self._db.collection(collection)
        if limit:
            docs = ref.limit(limit).stream()
        else:
            docs = ref.stream()
        try:
            docs_list = [doc.to_dict() for doc in docs]
            self._logger.info(f"Listed {len(docs_list)} documents from {collection}")
            return docs_list
        except Exception as e:
            self._logger.error(f"Error listing documents in {collection}: {e}")
            return []

database_manager = DatabaseManager()