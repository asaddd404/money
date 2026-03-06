from fastapi import HTTPException
from app.models.order import OrderStatus
from app.models.transaction import TransactionType
from app.repositories.orders import OrderRepository
from app.repositories.products import ProductRepository
from app.repositories.wallets import WalletRepository
from app.repositories.transactions import TransactionRepository
from app.repositories.idempotency import IdempotencyRepository
from app.services.audit_service import AuditService


class OrderService:
    def __init__(self, orders, products, wallets, tx, idem, audits):
        self.orders:OrderRepository=orders; self.products:ProductRepository=products; self.wallets:WalletRepository=wallets
        self.tx:TransactionRepository=tx; self.idem:IdempotencyRepository=idem; self.audits:AuditService=audits

    async def create(self, actor, items, idem_key, endpoint, method):
        cached=await self.idem.get(idem_key, actor.id, endpoint, method)
        if cached: return cached.status_code, cached.response_body
        total=0; loaded=[]
        for i in items:
            p=await self.products.get_for_update(i.product_id)
            if not p or p.center_id!=actor.center_id or p.stock < i.quantity: raise HTTPException(409,'stock not enough')
            p.stock -= i.quantity; total += p.price * i.quantity; loaded.append((p,i.quantity))
        w=await self.wallets.get_for_update(actor.id)
        if w.available_balance < total: raise HTTPException(409,'insufficient funds')
        w.available_balance -= total; w.held_balance += total
        o=await self.orders.create(center_id=actor.center_id, student_id=actor.id, status=OrderStatus.created, total_amount=total)
        for p,q in loaded:
            await self.orders.add_item(order_id=o.id, product_id=p.id, quantity=q, price_snapshot=p.price, product_name_snapshot=p.name)
        await self.tx.create(center_id=actor.center_id, student_id=actor.id, order_id=o.id, type=TransactionType.hold, amount=-total, reason='order hold', available_after=w.available_balance, held_after=w.held_balance)
        await self.audits.log(actor.center_id, actor.id, 'create_order', 'order', str(o.id), {'total': total})
        body={'id':o.id,'student_id':o.student_id,'status':o.status.value,'total_amount':o.total_amount}
        await self.idem.save(key=idem_key,user_id=actor.id,endpoint=endpoint,method=method,status_code=201,response_body=body)
        return 201, body

    async def set_status(self, actor, order_id:int, action:str):
        o=await self.orders.get(order_id)
        if not o or o.center_id!=actor.center_id: raise HTTPException(404,'order not found')
        mapping={'approve':OrderStatus.approved,'hand-over':OrderStatus.handed_over,'complete':OrderStatus.completed,'cancel':OrderStatus.cancelled,'reject':OrderStatus.rejected}
        if action in {'approve','hand-over','reject'} and actor.role not in {'manager','admin'}: raise HTTPException(403,'forbidden')
        if action in {'cancel','complete'} and actor.id!=o.student_id: raise HTTPException(403,'forbidden')
        if action in {'cancel','reject'}:
            w=await self.wallets.get_for_update(o.student_id)
            w.available_balance += o.total_amount; w.held_balance -= o.total_amount
            await self.tx.create(center_id=o.center_id, student_id=o.student_id, order_id=o.id, type=TransactionType.release, amount=o.total_amount, reason=action, available_after=w.available_balance, held_after=w.held_balance)
        if action=='complete':
            w=await self.wallets.get_for_update(o.student_id)
            w.held_balance -= o.total_amount; w.total_spent += o.total_amount
            await self.tx.create(center_id=o.center_id, student_id=o.student_id, order_id=o.id, type=TransactionType.purchase, amount=0, reason='complete', available_after=w.available_balance, held_after=w.held_balance)
        o.status=mapping[action]
        await self.audits.log(actor.center_id, actor.id, f'{action}_order', 'order', str(o.id), {'status': o.status.value})
        return o
