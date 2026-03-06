from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import current_user, db_dep
from app.models.order import Order, OrderStatus, OrderItem
from app.repositories.reviews import ReviewRepository
from app.schemas.review import ReviewCreate

router=APIRouter(tags=['reviews'])

@router.post('/products/{product_id}/reviews')
async def create_review(product_id:int,payload:ReviewCreate,user=Depends(current_user),db:AsyncSession=Depends(db_dep)):
    o=await db.get(Order,payload.order_id)
    if not o or o.center_id!=user.center_id or o.student_id!=user.id or o.status!=OrderStatus.completed: raise HTTPException(403,'review not allowed')
    item=await db.scalar(select(OrderItem).where(OrderItem.order_id==o.id, OrderItem.product_id==product_id))
    if not item: raise HTTPException(403,'product not in order')
    r=await ReviewRepository(db).create(center_id=user.center_id, product_id=product_id, order_id=o.id, student_id=user.id, rating=payload.rating, comment=payload.comment)
    await db.commit(); return {'id':r.id,'product_id':r.product_id,'order_id':r.order_id,'student_id':r.student_id,'rating':r.rating,'comment':r.comment}

@router.get('/products/{product_id}/reviews')
async def list_reviews(product_id:int,user=Depends(current_user),db:AsyncSession=Depends(db_dep)):
    rows=await ReviewRepository(db).list_by_product(user.center_id,product_id)
    return [{'id':r.id,'product_id':r.product_id,'order_id':r.order_id,'student_id':r.student_id,'rating':r.rating,'comment':r.comment} for r in rows]
