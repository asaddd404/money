from app.repositories.audits import AuditRepository


class AuditService:
    def __init__(self, repo: AuditRepository): self.repo = repo
    async def log(self, center_id:int, actor_user_id:int|None, action:str, entity_type:str, entity_id:str, payload:dict):
        return await self.repo.create(center_id=center_id, actor_user_id=actor_user_id, action=action, entity_type=entity_type, entity_id=entity_id, payload=payload)
