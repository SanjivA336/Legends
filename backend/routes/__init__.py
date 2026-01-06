from backend.database import *
from backend.models import *

def changes_to_string(changes: dict) -> str:
    messages = []
    for field, (old, new) in changes.items():
        messages.append(f"- **{field}** changed from '{old}' to '{new}'")
    return "\n".join(messages)

from .content_routes import router as content_router
from .game_routes import router as game_router
from .identity_routes import router as identity_router
from .timeline_routes import router as timeline_router

__all__ = [
    "content_router",
    "game_router",
    "identity_router",
    "timeline_router",
]