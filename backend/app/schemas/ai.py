from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    context: Optional[Dict[str, Any]] = None

class AnalyzeRequest(BaseModel):
    property: Dict[str, Any]
    preferences: Optional[Dict[str, Any]] = None

class ExtractRequest(BaseModel):
    text: str

class CompareRequest(BaseModel):
    properties: List[Dict[str, Any]]
    preferences: Optional[Dict[str, Any]] = None

class InsightRequest(BaseModel):
    location_id: str

class AIResponse(BaseModel):
    response: str
