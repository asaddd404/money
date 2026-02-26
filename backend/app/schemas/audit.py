from pydantic import BaseModel


class AuditOut(BaseModel):
    id: int
    action: str
    entity_type: str
    entity_id: str
    payload: dict
