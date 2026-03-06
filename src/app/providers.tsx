import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'sonner';
import { useEffect, useState, type PropsWithChildren } from 'react';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, staleTime: 30_000 }
  }
});

const ThemeProvider = ({ children }: PropsWithChildren) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark');
  }, [theme]);
  return (
    <div data-theme={theme}>
      <button
        aria-label="toggle-theme"
        className="fixed right-4 top-4 z-[60] rounded-full border bg-background px-3 py-2 text-xs"
        onClick={() => setTheme((p) => (p === 'light' ? 'dark' : 'light'))}
      >
        {theme === 'light' ? '🌙' : '☀️'}
      </button>
      {children}
    </div>
  );
};

export const AppProviders = ({ children }: PropsWithChildren) => (
  <QueryClientProvider client={queryClient}>
    <ThemeProvider>
      {children}
      <Toaster richColors position="top-right" />
    </ThemeProvider>
  </QueryClientProvider>
);
