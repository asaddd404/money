import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { CoinsAmount } from '@/components/common';
import { OrderStatusBadge } from '@/components/badges';
import type { Order, Product } from '@/api/types';

export const ProductCard = ({ product, onAction, actionLabel = 'View' }: { product: Product; onAction: () => void; actionLabel?: string }) => (
  <Card className="space-y-3">
    <div className="flex items-start justify-between gap-3"><h3 className="font-medium">{product.title}</h3><CoinsAmount amount={product.price_coins} /></div>
    <p className="text-sm text-muted-foreground">{product.description}</p>
    <Button className="w-full" onClick={onAction}>{actionLabel}</Button>
  </Card>
);

export const ProductRow = ({ product, onAction }: { product: Product; onAction: () => void }) => (
  <div className="hidden items-center justify-between border-b py-3 md:flex"><div><p className="font-medium">{product.title}</p><p className="text-sm text-muted-foreground">Stock: {product.stock}</p></div><div className="flex items-center gap-3"><CoinsAmount amount={product.price_coins} /><Button onClick={onAction}>Manage</Button></div></div>
);

export const EnrollmentCard = ({ name, onApprove, onReject }: { name: string; onApprove: () => void; onReject: () => void }) => (
  <Card><p className="font-medium">{name}</p><div className="mt-3 grid grid-cols-2 gap-2"><Button onClick={onApprove}>Approve</Button><Button variant="outline" onClick={onReject}>Reject</Button></div></Card>
);

export const EnrollmentRow = ({ name, onApprove, onReject }: { name: string; onApprove: () => void; onReject: () => void }) => (
  <div className="hidden items-center justify-between border-b py-3 md:flex"><span>{name}</span><div className="flex gap-2"><Button onClick={onApprove}>Approve</Button><Button variant="outline" onClick={onReject}>Reject</Button></div></div>
);

export const OrderCard = ({ order, onAction }: { order: Order; onAction?: () => void }) => (
  <Card><div className="flex items-center justify-between"><p className="font-medium">Order #{order.id.slice(0, 8)}</p><OrderStatusBadge status={order.status} /></div>{onAction && <Button className="mt-3 w-full" onClick={onAction}>Open</Button>}</Card>
);

export const OrdersTable = ({ orders }: { orders: Order[] }) => (
  <div className="hidden md:block"><div className="rounded-xl border">{orders.map((order) => <div key={order.id} className="grid grid-cols-3 border-b p-3"><span>{order.id.slice(0, 8)}</span><OrderStatusBadge status={order.status} /><span>{new Date(order.created_at).toLocaleDateString()}</span></div>)}</div></div>
);
