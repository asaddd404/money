import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { LoginPage } from '@/features/auth/LoginPage';
import { http } from '@/api/http';

vi.mock('@/api/http', async () => {
  const actual = await vi.importActual<any>('@/api/http');
  return {
    ...actual,
    http: {
      ...actual.http,
      post: vi.fn(),
      get: vi.fn()
    }
  };
});

describe('login flow', () => {
  it('navigates to role home after login', async () => {
    (http.post as any).mockResolvedValue({ data: { access_token: 'a', refresh_token: 'r' } });
    (http.get as any).mockResolvedValue({ data: { id: '1', full_name: 'Test', email: 't@t.com', role: 'teacher' } });

    render(
      <QueryClientProvider client={new QueryClient()}>
        <MemoryRouter initialEntries={['/auth/login']}>
          <Routes>
            <Route path="/auth/login" element={<LoginPage />} />
            <Route path="/app/teacher/home" element={<div>Teacher Home</div>} />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>
    );

    fireEvent.change(screen.getByPlaceholderText(/email/i), { target: { value: 't@t.com' } });
    fireEvent.change(screen.getByPlaceholderText(/password/i), { target: { value: '1234' } });
    fireEvent.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => expect(screen.getByText(/Teacher Home/i)).toBeInTheDocument());
  });
});
