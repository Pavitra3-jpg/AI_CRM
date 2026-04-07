from pydantic import BaseModel
from typing import Optional

class InteractionSchema(BaseModel):
    hcp_name: str
    interaction_type: str
    product: Optional[str] = ""
    notes: Optional[str] = ""
    sentiment: Optional[str] = ""
    concerns: Optional[str] = ""
    follow_up: Optional[str] = ""

class ChatInput(BaseModel):
    text: str