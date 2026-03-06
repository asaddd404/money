import { api } from './client';

export async function login(email: string, password: string) {
  const { data } = await api.post('/auth/login', { email, password });
  return data as { access_token: string; refresh_token: string; token_type: string };
}

export async function getMe() {
  const { data } = await api.get('/users/me');
  return data;
}
