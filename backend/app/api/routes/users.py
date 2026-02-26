from fastapi import APIRouter, Depends
from app.api.deps import current_user

router = APIRouter(prefix='/users', tags=['users'])

@router.get('/me')
async def me(user=Depends(current_user)):
    return {'id':user.id,'center_id':user.center_id,'email':user.email,'full_name':user.full_name,'role':user.role.value}
