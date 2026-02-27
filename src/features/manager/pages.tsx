import { useMutation, useQuery } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { endpoints } from '@/api/endpoints';
import { http } from '@/api/http';
import { type Order, type Product } from '@/api/types';
import { PageHeader } from '@/components/common';
import {
  OrderCard,
  OrdersTable,
  ProductCard,
  ProductRow
} from '@/components/entity-cards';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

interface ProductPayload {
  title: string;
  description: string;
  price_coins: number;
  stock: number;
}

interface AuditLogItem {
  id: string;
  action: string;
}

export const ManagerHomePage = () => (
  <div className="space-y-3">
    <PageHeader title="Manager Home" />
    <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
      <div className="rounded-xl border p-4">Pending enrollments</div>
      <div className="rounded-xl border p-4">Orders queue</div>
      <div className="rounded-xl border p-4">Low stock</div>
    </div>
  </div>
);

export const ManagerProductsPage = () => {
  const { data, refetch } = useQuery<{ items: Product[] }>({
    queryKey: ['manager-products'],
    queryFn: async () => (await http.get(endpoints.products)).data
  });
  const { register, handleSubmit, reset } = useForm<ProductPayload>();
  const create = useMutation({
    mutationFn: (body: ProductPayload) => http.post(endpoints.products, body),
    onSuccess: () => {
      reset();
      refetch();
    }
  });
  const remove = useMutation({
    mutationFn: (id: string) => http.delete(`${endpoints.products}/${id}`),
    onSuccess: () => refetch()
  });
  return (
    <div className="space-y-3">
      <PageHeader title="Products" />
      <form
        className="space-y-2 rounded-xl border p-3"
        onSubmit={handleSubmit((v) => create.mutate(v))}
      >
        <Input placeholder="Title" {...register('title')} />
        <Input placeholder="Description" {...register('description')} />
        <Input
          type="number"
          placeholder="Price"
          {...register('price_coins', { valueAsNumber: true })}
        />
        <Input
          type="number"
          placeholder="Stock"
          {...register('stock', { valueAsNumber: true })}
        />
        <Button className="w-full">Create product</Button>
      </form>
      {(data?.items ?? []).map((p) => (
        <div key={p.id}>
          <ProductCard
            product={p}
            onAction={() => remove.mutate(p.id)}
            actionLabel="Delete"
          />
          <ProductRow product={p} onAction={() => remove.mutate(p.id)} />
        </div>
      ))}
    </div>
  );
};

export const ManagerOrdersPage = () => {
  const { data } = useQuery<{ items: Order[] }>({
    queryKey: ['manager-orders'],
    queryFn: async () => (await http.get(endpoints.orders)).data
  });
  const action = useMutation({
    mutationFn: ({ id, step }: { id: string; step: string }) =>
      http.post(`${endpoints.orders}/${id}/${step}`)
  });
  const orders = data?.items ?? [];
  return (
    <div className="space-y-3">
      <PageHeader title="Orders queue" />
      {orders.map((order) => (
        <OrderCard
          key={order.id}
          order={order}
          onAction={() => action.mutate({ id: order.id, step: 'approve' })}
        />
      ))}
      <OrdersTable orders={orders} />
    </div>
  );
};

export const ManagerAuditPage = () => {
  const { data } = useQuery<{ items: AuditLogItem[] }>({
    queryKey: ['audit'],
    queryFn: async () =>
      (
        await http.get(endpoints.admin.auditLogs, {
          params: { limit: 20, offset: 0 }
        })
      ).data,
    retry: false
  });
  return (
    <div className="space-y-3">
      <PageHeader title="Audit logs" />
      {(data?.items ?? []).map((l) => (
        <div key={l.id} className="rounded-xl border p-3 text-xs">
          {l.action}
        </div>
      ))}
    </div>
  );
};
