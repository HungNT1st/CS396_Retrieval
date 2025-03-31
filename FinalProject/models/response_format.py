from pydantic import BaseModel

class ContextualFormat(BaseModel):
    nationality: str
    mission: str
    activities: str