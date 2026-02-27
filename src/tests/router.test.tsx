import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { AppRouter } from '@/app/router';
import { useAuthStore } from '@/store/auth.store';

describe('routing guards', () => {
  beforeEach(() => useAuthStore.setState({ accessToken: null, refreshToken: null, user: null, role: null }));

  it('protected route redirect to login', () => {
    render(<MemoryRouter initialEntries={['/app/student/home']}><AppRouter /></MemoryRouter>);
    expect(screen.getByText(/sign in/i)).toBeInTheDocument();
  });

  it('role redirect when forbidden page', () => {
    useAuthStore.setState({ role: 'student', accessToken: 'a', refreshToken: null, user: { id: '1', full_name: 'A', email: 'a@a.com', role: 'student' } });
    render(<MemoryRouter initialEntries={['/app/admin/home']}><AppRouter /></MemoryRouter>);
    expect(screen.getByText(/Student Home/i)).toBeInTheDocument();
  });
});
