import { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis } from 'recharts';
import { endpoints } from '@/api/endpoints';
import { http, postWithIdempotency } from '@/api/http';
import { PageHeader, PeriodPicker, SearchInput } from '@/components/common';
import { EmptyState, ErrorState, LoadingSkeleton } from '@/components/data-states';
import { OrderCard, OrdersTable, ProductCard } from '@/components/entity-cards';
import { Button } from '@/components/ui/button';
import { useDebouncedSearch } from '@/hooks/useDebouncedSearch';
import { useCreateOrder, useOrders, useProducts } from '@/features/common/api';

interface WalletSummary {
  available: number;
  held: number;
}

interface TransactionItem {
  id: string;
  reason: string;
  amount: number;
}

interface GroupItem {
  id: string;
  name: string;
}

interface LeaderboardItem {
  name: string;
  coins: number;
}

export const StudentHomePage = () => {
  const { data, isLoading } = useQuery<WalletSummary>({
    queryKey: ['wallet-summary'],
    queryFn: async () => (await http.get('/students/me/wallet')).data
  });
export const StudentHomePage = () => {
  const { data, isLoading } = useQuery({ queryKey: ['wallet-summary'], queryFn: async () => (await http.get('/students/me/wallet')).data });
  if (isLoading) return <LoadingSkeleton />;
  return <div className="space-y-4"><PageHeader title="Student Home" /><div className="grid grid-cols-2 gap-3"><div className="rounded-xl border p-4">Available: {data?.available ?? 0}</div><div className="rounded-xl border p-4">Held: {data?.held ?? 0}</div></div></div>;
};

export const StudentWalletPage = () => {
  const { data, isLoading, error } = useQuery<WalletSummary>({ queryKey: ['wallet'], queryFn: async () => (await http.get('/students/me/wallet')).data });
  const { data, isLoading, error } = useQuery({ queryKey: ['wallet'], queryFn: async () => (await http.get('/students/me/wallet')).data });
  if (isLoading) return <LoadingSkeleton />;
  if (error) return <ErrorState message={(error as Error).message} />;
  return <div className="space-y-3"><PageHeader title="Wallet" /><pre className="rounded-xl border p-4 text-sm">{JSON.stringify(data, null, 2)}</pre></div>;
};

export const StudentTransactionsPage = () => {
  const [offset, setOffset] = useState(0);
  const { data, isLoading } = useQuery<{ items: TransactionItem[] }>({ queryKey: ['tx', offset], queryFn: async () => (await http.get('/students/me/transactions', { params: { limit: 20, offset } })).data });
  if (isLoading) return <LoadingSkeleton />;
  return <div className="space-y-3"><PageHeader title="Transactions" />{(data?.items ?? []).map((tx) => <div className="rounded-xl border p-3" key={tx.id}>{tx.reason} — {tx.amount}</div>)}<Button variant="outline" onClick={() => setOffset((p) => p + 20)}>Load more</Button></div>;
};

export const StudentGroupsPage = () => {
  const { data } = useQuery<{ items: GroupItem[] }>({ queryKey: ['groups'], queryFn: async () => (await http.get(endpoints.groups, { params: { limit: 20, offset: 0 } })).data });
  const enrollMutation = useMutation({ mutationFn: (groupId: string) => postWithIdempotency(`${endpoints.groups}/${groupId}/enroll`, {}) });
  return <div className="space-y-3"><PageHeader title="Groups" />{(data?.items ?? []).map((g) => <div key={g.id} className="rounded-xl border p-4"><p>{g.name}</p><Button className="mt-3 w-full" disabled={enrollMutation.isPending} onClick={() => enrollMutation.mutate(g.id)}>{enrollMutation.isPending ? 'Pending...' : 'Enroll request'}</Button></div>)}</div>;

  const { data, isLoading } = useQuery({ queryKey: ['tx', offset], queryFn: async () => (await http.get('/students/me/transactions', { params: { limit: 20, offset } })).data });
  if (isLoading) return <LoadingSkeleton />;
  return <div className="space-y-3"><PageHeader title="Transactions" />{(data?.items ?? []).map((tx: any) => <div className="rounded-xl border p-3" key={tx.id}>{tx.reason} — {tx.amount}</div>)}<Button variant="outline" onClick={() => setOffset((p) => p + 20)}>Load more</Button></div>;
};

export const StudentGroupsPage = () => {
  const { data } = useQuery({ queryKey: ['groups'], queryFn: async () => (await http.get(endpoints.groups, { params: { limit: 20, offset: 0 } })).data });
  const enrollMutation = useMutation({ mutationFn: (groupId: string) => postWithIdempotency(`${endpoints.groups}/${groupId}/enroll`, {}) });
  return <div className="space-y-3"><PageHeader title="Groups" />{(data?.items ?? []).map((g: any) => <div key={g.id} className="rounded-xl border p-4"><p>{g.name}</p><Button className="mt-3 w-full" disabled={enrollMutation.isPending} onClick={() => enrollMutation.mutate(g.id)}>{enrollMutation.isPending ? 'Pending...' : 'Enroll request'}</Button></div>)}</div>;
};

export const StudentShopPage = () => {
  const [offset, setOffset] = useState(0);
  const { value, query, onChange } = useDebouncedSearch();
  const { data, isLoading } = useProducts(20, offset, query);
  const createOrder = useCreateOrder();
  if (isLoading) return <LoadingSkeleton />;
  return <div className="space-y-3"><PageHeader title="Shop" /><SearchInput value={value} onChange={onChange} />{(data?.items ?? []).map((p) => <ProductCard key={p.id} product={p} onAction={() => createOrder.mutate({ product_id: p.id, quantity: 1 })} actionLabel={createOrder.isPending ? 'Pending...' : 'Create order'} />)}<Button variant="outline" onClick={() => setOffset((p) => p + 20)}>Load more</Button></div>;
};

export const StudentOrdersPage = () => {
  const { data } = useOrders();
  const cancel = useMutation({ mutationFn: (id: string) => http.post(`${endpoints.orders}/${id}/cancel`) });
  const orders = data?.items ?? [];
  if (!orders.length) return <EmptyState title="No orders yet" description="Purchase products from shop" />;
  return <div className="space-y-3"><PageHeader title="Orders" />{orders.map((order) => <OrderCard key={order.id} order={order} onAction={() => cancel.mutate(order.id)} />)}<OrdersTable orders={orders} /></div>;
};

export const StudentLeaderboardsPage = () => {
  const [period, setPeriod] = useState('week');
  const { data } = useQuery<{ items: LeaderboardItem[] }>({ queryKey: ['leaderboard', period], queryFn: async () => (await http.get(`${endpoints.leaderboards}/global`, { params: { period } })).data });
  const { data } = useQuery({ queryKey: ['leaderboard', period], queryFn: async () => (await http.get(`${endpoints.leaderboards}/global`, { params: { period } })).data });
  return <div className="space-y-3"><PageHeader title="Leaderboards" /><PeriodPicker value={period} onChange={setPeriod} /><div className="h-72 rounded-xl border p-2"><ResponsiveContainer width="100%" height="100%"><BarChart data={data?.items ?? []}><XAxis dataKey="name" hide /><YAxis /><Bar dataKey="coins" fill="hsl(var(--primary))" radius={[6,6,0,0]} /></BarChart></ResponsiveContainer></div></div>;
};
