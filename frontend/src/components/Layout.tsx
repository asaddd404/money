import { Link, Outlet } from 'react-router-dom';

export function Layout() {
  return (
    <div style={{ maxWidth: 960, margin: '0 auto', padding: 16, fontFamily: 'sans-serif' }}>
      <header style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
        <Link to="/">Dashboard</Link>
        <Link to="/login">Login</Link>
      </header>
      <Outlet />
    </div>
  );
}
