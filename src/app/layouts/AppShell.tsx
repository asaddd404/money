import { Link, Outlet, useLocation } from 'react-router-dom';
import { Home, ShoppingBag, Trophy, Users, Settings, Menu } from 'lucide-react';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { useAuthStore } from '@/store/auth.store';
import { RoleBadge } from '@/components/badges';

const navByRole = {
  student: [
    { to: '/app/student/home', label: 'Home', icon: Home },
    { to: '/app/student/shop', label: 'Shop', icon: ShoppingBag },
    { to: '/app/student/groups', label: 'Groups', icon: Users },
    { to: '/app/student/leaderboards', label: 'Top', icon: Trophy },
    { to: '/app/student/settings', label: 'More', icon: Settings }
  ],
  teacher: [
    { to: '/app/teacher/home', label: 'Home', icon: Home },
    { to: '/app/teacher/groups', label: 'Groups', icon: Users },
    { to: '/app/teacher/award', label: 'Award', icon: ShoppingBag },
    { to: '/app/teacher/leaderboards', label: 'Top', icon: Trophy },
    { to: '/app/teacher/settings', label: 'More', icon: Settings }
  ],
  manager: [
    { to: '/app/manager/home', label: 'Home', icon: Home },
    { to: '/app/manager/products', label: 'Products', icon: ShoppingBag },
    { to: '/app/manager/orders', label: 'Orders', icon: Users },
    { to: '/app/manager/audit', label: 'Audit', icon: Trophy },
    { to: '/app/manager/settings', label: 'More', icon: Settings }
  ],
  admin: [
    { to: '/app/admin/home', label: 'Home', icon: Home },
    { to: '/app/admin/products', label: 'Products', icon: ShoppingBag },
    { to: '/app/admin/orders', label: 'Orders', icon: Users },
    { to: '/app/admin/policies', label: 'Policies', icon: Trophy },
    { to: '/app/admin/settings', label: 'More', icon: Settings }
  ]
} as const;

export const AppShell = () => {
  const role = useAuthStore((s) => s.role) ?? 'student';
  const user = useAuthStore((s) => s.user);
  const location = useLocation();
  const nav = navByRole[role];

  return (
    <div className="mx-auto flex min-h-screen max-w-7xl bg-background">
      <aside className="hidden w-64 border-r p-4 md:block">
        <p className="mb-4 text-lg font-semibold">Money Platform</p>
        <div className="space-y-1">
          {nav.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className={`block rounded-md px-3 py-3 text-sm ${location.pathname.startsWith(item.to) ? 'bg-primary text-primary-foreground' : 'hover:bg-muted'}`}
            >
              {item.label}
            </Link>
          ))}
        </div>
      </aside>
      <main className="flex-1 pb-20 md:pb-6">
        <header className="sticky top-0 z-40 flex items-center justify-between border-b bg-background/90 px-4 py-3 backdrop-blur">
          <div>
            <p className="font-semibold">{user?.full_name ?? 'User'}</p>
            <RoleBadge role={role} />
          </div>
          <Sheet>
            <SheetTrigger asChild>
              <button className="rounded-md border p-2 md:hidden">
                <Menu className="size-4" />
              </button>
            </SheetTrigger>
            <SheetContent>
              <div className="space-y-2 pt-6">
                {nav.map((item) => (
                  <Link
                    key={item.to}
                    to={item.to}
                    className="block rounded-md border px-3 py-3"
                  >
                    {item.label}
                  </Link>
                ))}
              </div>
            </SheetContent>
          </Sheet>
        </header>
        <div className="p-4">
          <Outlet />
        </div>
      </main>
      <nav className="fixed bottom-0 left-0 right-0 z-50 grid grid-cols-5 border-t bg-background md:hidden">
        {nav.map((item) => {
          const Icon = item.icon;
          const active = location.pathname.startsWith(item.to);
          return (
            <Link
              key={item.to}
              to={item.to}
              className={`flex min-h-14 flex-col items-center justify-center text-xs ${active ? 'text-primary' : 'text-muted-foreground'}`}
            >
              <Icon className="mb-1 size-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </div>
  );
};
