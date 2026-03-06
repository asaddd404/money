import { Outlet } from 'react-router-dom';

export const AuthLayout = () => (
  <div className="flex min-h-screen items-center justify-center bg-muted/30 p-4">
    <div className="w-full max-w-md rounded-2xl border bg-card p-5 shadow-sm">
      <Outlet />
    </div>
  </div>
);
