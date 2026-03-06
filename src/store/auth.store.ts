import { create } from 'zustand';
import type { Role, User } from '@/api/types';

interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  user: User | null;
  role: Role | null;
  setSession: (payload: {
    accessToken: string;
    refreshToken?: string;
    user?: User;
  }) => void;
  setUser: (user: User) => void;
  logout: () => void;
}

const enableSessionStorage =
  import.meta.env.VITE_ENABLE_REFRESH_SESSION_STORAGE === 'true';

export const useAuthStore = create<AuthState>((set) => ({
  accessToken: null,
  refreshToken: enableSessionStorage
    ? sessionStorage.getItem('refreshToken')
    : null,
  user: null,
  role: null,
  setSession: ({ accessToken, refreshToken, user }) => {
    if (enableSessionStorage && refreshToken)
      sessionStorage.setItem('refreshToken', refreshToken);
    set({
      accessToken,
      refreshToken: refreshToken ?? null,
      user: user ?? null,
      role: user?.role ?? null
    });
  },
  setUser: (user) => set({ user, role: user.role }),
  logout: () => {
    if (enableSessionStorage) sessionStorage.removeItem('refreshToken');
    set({ accessToken: null, refreshToken: null, user: null, role: null });
  }
}));
