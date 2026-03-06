import { api } from './client';
import type { Group, LeaderboardRow, Product } from '../types/api';

export async function getGroups(): Promise<Group[]> {
  const { data } = await api.get('/groups');
  return data;
}

export async function getProducts(): Promise<Product[]> {
  const { data } = await api.get('/products');
  return data;
}

export async function getGlobalLeaderboard(period: 'day' | 'week' | 'month'): Promise<LeaderboardRow[]> {
  const { data } = await api.get('/leaderboards/global', { params: { period } });
  return data;
}
