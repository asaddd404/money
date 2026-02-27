export type Role = 'student' | 'teacher' | 'manager' | 'admin';

export interface ApiErrorPayload {
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
}

export interface User {
  id: string;
  full_name: string;
  email: string;
  role: Role;
}

export interface Tokens {
  access_token: string;
  refresh_token?: string;
}

export interface Paginated<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

export interface Product {
  id: string;
  title: string;
  description: string;
  price_coins: number;
  stock: number;
  image_url?: string;
}

export interface Order {
  id: string;
  product_id: string;
  status: 'pending' | 'approved' | 'rejected' | 'handed_over' | 'cancelled' | 'completed';
  quantity: number;
  created_at: string;
}
