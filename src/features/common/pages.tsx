import { useNavigate } from 'react-router-dom';
import { useMe } from '@/features/common/api';
import { PageHeader } from '@/components/common';
import { LoadingSkeleton, ErrorState } from '@/components/data-states';
import { Button } from '@/components/ui/button';
import { useAuthStore } from '@/store/auth.store';

export const ProfilePage = () => {
  const { data, isLoading, error } = useMe();
  if (isLoading) return <LoadingSkeleton />;
  if (error) return <ErrorState message={(error as Error).message} />;
  return <div className="space-y-3"><PageHeader title="Profile" /><p className="rounded-xl border p-4">{data?.full_name} ({data?.email})</p></div>;
};

export const SettingsPage = () => {
  const logout = useAuthStore((s) => s.logout);
  const navigate = useNavigate();
  return <div className="space-y-3"><PageHeader title="Settings" /><Button variant="destructive" onClick={() => { logout(); navigate('/auth/login'); }}>Logout</Button></div>;
};

export const NotFoundPage = () => <div className="space-y-2"><h1 className="text-2xl font-semibold">404</h1><p className="text-muted-foreground">Page not found.</p></div>;
export const GlobalErrorPage = () => <div className="space-y-2"><h1 className="text-2xl font-semibold">Something broke</h1><p className="text-muted-foreground">Try refreshing the page.</p></div>;
