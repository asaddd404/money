from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import current_user, db_dep, idem_header
from app.repositories.orders import OrderRepository
from app.repositories.products import ProductRepository
from app.repositories.wallets import WalletRepository
from app.repositories.transactions import TransactionRepository
from app.repositories.idempotency import IdempotencyRepository
from app.repositories.audits import AuditRepository
from app.schemas.order import OrderCreateIn
from app.services.order_service import OrderService
from app.services.audit_service import AuditService

router=APIRouter(prefix='/orders', tags=['orders'])

@router.post('')
async def create_order(payload:OrderCreateIn,idempotency_key:str=Depends(idem_header),user=Depends(current_user),db:AsyncSession=Depends(db_dep)):
    if user.role.value!='student': raise HTTPException(403,'forbidden')
    svc=OrderService(OrderRepository(db),ProductRepository(db),WalletRepository(db),TransactionRepository(db),IdempotencyRepository(db),AuditService(AuditRepository(db)))
    code,body=await svc.create(user,payload.items,idempotency_key,'/api/v1/orders','POST')
    await db.commit(); return JSONResponse(status_code=code, content=body)

@router.get('')
async def list_orders(limit:int=20, offset:int=0, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    rows=await OrderRepository(db).list(user.center_id,limit,offset)
    return [{'id':o.id,'student_id':o.student_id,'status':o.status.value,'total_amount':o.total_amount} for o in rows]

@router.get('/{id}')
async def get_order(id:int, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    o=await OrderRepository(db).get(id)
    if not o or o.center_id!=user.center_id: raise HTTPException(404,'order not found')
    return {'id':o.id,'student_id':o.student_id,'status':o.status.value,'total_amount':o.total_amount}

@router.post('/{id}/approve')
async def approve(id:int, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    o=await OrderService(OrderRepository(db),ProductRepository(db),WalletRepository(db),TransactionRepository(db),IdempotencyRepository(db),AuditService(AuditRepository(db))).set_status(user,id,'approve')
    await db.commit(); return {'id':o.id,'status':o.status.value}

@router.post('/{id}/hand-over')
async def hand_over(id:int, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    o=await OrderService(OrderRepository(db),ProductRepository(db),WalletRepository(db),TransactionRepository(db),IdempotencyRepository(db),AuditService(AuditRepository(db))).set_status(user,id,'hand-over')
    await db.commit(); return {'id':o.id,'status':o.status.value}

@router.post('/{id}/complete')
async def complete(id:int, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    o=await OrderService(OrderRepository(db),ProductRepository(db),WalletRepository(db),TransactionRepository(db),IdempotencyRepository(db),AuditService(AuditRepository(db))).set_status(user,id,'complete')
    await db.commit(); return {'id':o.id,'status':o.status.value}

@router.post('/{id}/cancel')
async def cancel(id:int, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    o=await OrderService(OrderRepository(db),ProductRepository(db),WalletRepository(db),TransactionRepository(db),IdempotencyRepository(db),AuditService(AuditRepository(db))).set_status(user,id,'cancel')
    await db.commit(); return {'id':o.id,'status':o.status.value}
