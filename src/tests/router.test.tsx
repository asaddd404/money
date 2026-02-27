import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { AppRouter } from '@/app/router';
import { useAuthStore } from '@/store/auth.store';

vi.mock('@/api/http', async () => {
  const actual = await vi.importActual<typeof import('@/api/http')>('@/api/http');
  return {
    ...actual,
    http: {
      ...actual.http,
      get: vi.fn().mockResolvedValue({ data: { available: 0, held: 0 } }),
      post: vi.fn()
    }
  };
});

describe('routing guards', () => {
  beforeEach(() =>
    useAuthStore.setState({
      accessToken: null,
      refreshToken: null,
      user: null,
      role: null
    })
  );

  const renderRouter = (initialEntry: string) =>
    render(
      <QueryClientProvider client={new QueryClient()}>
        <MemoryRouter initialEntries={[initialEntry]}>
          <AppRouter />
        </MemoryRouter>
      </QueryClientProvider>
    );

  it('protected route redirect to login', () => {
    renderRouter('/app/student/home');
    expect(
      screen.getByRole('heading', { name: /sign in/i, level: 1 })
    ).toBeInTheDocument();
  });

  it('role redirect when forbidden page', async () => {
    useAuthStore.setState({
      role: 'student',
      accessToken: 'a',
      refreshToken: null,
      user: {
        id: '1',
        full_name: 'A',
        email: 'a@a.com',
        role: 'student'
      }
    });
    renderRouter('/app/admin/home');
    expect(await screen.findByText(/Student Home/i)).toBeInTheDocument();
  });
});
