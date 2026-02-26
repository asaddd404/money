from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import current_user, db_dep
from app.repositories.groups import GroupRepository
from app.schemas.group import GroupCreate, GroupPatch

router=APIRouter(prefix='/groups', tags=['groups'])

@router.get('')
async def list_groups(limit:int=20, offset:int=0, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    return [ {'id':g.id,'center_id':g.center_id,'name':g.name,'owner_teacher_id':g.owner_teacher_id} for g in await GroupRepository(db).list(user.center_id,limit,offset) ]

@router.post('')
async def create_group(payload:GroupCreate, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    if user.role.value not in {'manager','admin'}: raise HTTPException(403,'forbidden')
    g=await GroupRepository(db).create(center_id=user.center_id,name=payload.name,owner_teacher_id=payload.owner_teacher_id)
    await db.commit(); return {'id':g.id,'center_id':g.center_id,'name':g.name,'owner_teacher_id':g.owner_teacher_id}

@router.patch('/{id}')
async def patch_group(id:int, payload:GroupPatch, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    g=await GroupRepository(db).get(id)
    if not g or g.center_id!=user.center_id: raise HTTPException(404,'group not found')
    if user.role.value not in {'manager','admin'}: raise HTTPException(403,'forbidden')
    if payload.name is not None: g.name=payload.name
    if payload.owner_teacher_id is not None: g.owner_teacher_id=payload.owner_teacher_id
    await db.commit(); return {'id':g.id,'center_id':g.center_id,'name':g.name,'owner_teacher_id':g.owner_teacher_id}

@router.delete('/{id}')
async def delete_group(id:int, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    g=await GroupRepository(db).get(id)
    if not g or g.center_id!=user.center_id: raise HTTPException(404,'group not found')
    if user.role.value not in {'manager','admin'}: raise HTTPException(403,'forbidden')
    await db.delete(g); await db.commit(); return {'ok':True}
