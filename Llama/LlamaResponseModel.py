from pydantic import BaseModel
from typing import Optional

class Message(BaseModel):
    role: str
    content: str

class LlamaResponse(BaseModel):
    model: str
    created_at: str
    message: Message
    done: bool
    done_reason: Optional[str] = None
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None
    
class LlamaResponseList(BaseModel):
    list: list[LlamaResponse]