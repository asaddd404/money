from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import current_user, db_dep
from app.repositories.products import ProductRepository
from app.schemas.product import ProductCreate, ProductPatch

router=APIRouter(prefix='/products', tags=['products'])

@router.get('')
async def list_products(limit:int=20, offset:int=0, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    rows=await ProductRepository(db).list(user.center_id, limit, offset)
    return [{'id':p.id,'name':p.name,'price':p.price,'stock':p.stock,'is_active':p.is_active} for p in rows]

@router.post('')
async def create_product(payload:ProductCreate, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    if user.role.value not in {'manager','admin'}: raise HTTPException(403,'forbidden')
    p=await ProductRepository(db).create(center_id=user.center_id, name=payload.name, price=payload.price, stock=payload.stock)
    await db.commit(); return {'id':p.id,'name':p.name,'price':p.price,'stock':p.stock,'is_active':p.is_active}

@router.patch('/{id}')
async def patch_product(id:int,payload:ProductPatch,user=Depends(current_user),db:AsyncSession=Depends(db_dep)):
    p=await ProductRepository(db).get(id)
    if not p or p.center_id!=user.center_id: raise HTTPException(404,'product not found')
    if user.role.value not in {'manager','admin'}: raise HTTPException(403,'forbidden')
    for f in ['name','price','stock','is_active']:
        v=getattr(payload,f)
        if v is not None: setattr(p,f,v)
    await db.commit(); return {'id':p.id,'name':p.name,'price':p.price,'stock':p.stock,'is_active':p.is_active}

@router.delete('/{id}')
async def delete_product(id:int,user=Depends(current_user),db:AsyncSession=Depends(db_dep)):
    p=await ProductRepository(db).get(id)
    if not p or p.center_id!=user.center_id: raise HTTPException(404,'product not found')
    if user.role.value not in {'manager','admin'}: raise HTTPException(403,'forbidden')
    await db.delete(p); await db.commit(); return {'ok':True}
