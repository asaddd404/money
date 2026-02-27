import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { endpoints } from '@/api/endpoints';
import { http, postWithIdempotency } from '@/api/http';
import type { Order, Paginated, Product, User } from '@/api/types';

export const useMe = () =>
  useQuery({
    queryKey: ['me'],
    queryFn: async () => (await http.get<User>(endpoints.users.me)).data
  });

export const useProducts = (limit = 20, offset = 0, search = '') =>
  useQuery({
    queryKey: ['products', limit, offset, search],
    queryFn: async () =>
      (
        await http.get<Paginated<Product>>(endpoints.products, {
          params: { limit, offset, search }
        })
      ).data
  });

export const useOrders = (limit = 20, offset = 0) =>
  useQuery({
    queryKey: ['orders', limit, offset],
    queryFn: async () =>
      (
        await http.get<Paginated<Order>>(endpoints.orders, {
          params: { limit, offset }
        })
      ).data
  });

export const useCreateOrder = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: { product_id: string; quantity: number }) =>
      postWithIdempotency<Order>(endpoints.orders, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['orders'] })
  });
};
