import axios, { AxiosError, AxiosHeaders, type InternalAxiosRequestConfig } from 'axios';
import { toast } from 'sonner';
import { useAuthStore } from '@/store/auth.store';
import type { ApiErrorPayload, Tokens } from '@/api/types';

const apiUrl = `${import.meta.env.VITE_API_URL}/api/v1`;

class ApiError extends Error {
  code: string;
  details?: Record<string, unknown>;
  constructor(payload: ApiErrorPayload['error']) {
    super(payload.message);
    this.code = payload.code;
    this.details = payload.details;
  }
}

let refreshPromise: Promise<string | null> | null = null;

const parseApiError = (error: unknown) => {
  const fallback = new ApiError({ code: 'UNKNOWN_ERROR', message: 'Something went wrong' });
  if (!axios.isAxiosError(error)) return fallback;
  const payload = error.response?.data as ApiErrorPayload | undefined;
  if (payload?.error) {
    const parsed = new ApiError(payload.error);
    if (import.meta.env.DEV) console.error('API_ERROR_CODE', parsed.code, parsed.details);
    return parsed;
  }
  return fallback;
};

export const http = axios.create({
  baseURL: apiUrl,
  withCredentials: true
});

const refreshToken = async () => {
  const store = useAuthStore.getState();
  if (!store.refreshToken) return null;
  const { data } = await axios.post<Tokens>(`${apiUrl}/auth/refresh`, { refresh_token: store.refreshToken }, { withCredentials: true });
  store.setSession({ accessToken: data.access_token, refreshToken: data.refresh_token ?? store.refreshToken });
  return data.access_token;
};

http.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = useAuthStore.getState().accessToken;
  if (token) {
    config.headers = new AxiosHeaders(config.headers);
    config.headers.set('Authorization', `Bearer ${token}`);
  }
  return config;
});

http.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const original = error.config as InternalAxiosRequestConfig & { _retry?: boolean };
    if (error.response?.status === 401 && !original?._retry) {
      original._retry = true;
      refreshPromise = refreshPromise ?? refreshToken().finally(() => (refreshPromise = null));
      const nextAccess = await refreshPromise;
      if (nextAccess) {
        original.headers = new AxiosHeaders(original.headers);
        original.headers.set('Authorization', `Bearer ${nextAccess}`);
        return http(original);
      }
      useAuthStore.getState().logout();
      window.location.href = '/auth/login';
    }
    const parsedError = parseApiError(error);
    toast.error(parsedError.message);
    throw parsedError;
  }
);

export const postWithIdempotency = <T>(url: string, body: unknown) =>
  http.post<T>(url, body, { headers: { 'Idempotency-Key': crypto.randomUUID() } });

export { ApiError };
