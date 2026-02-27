import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { z } from 'zod';
import { endpoints } from '@/api/endpoints';
import { http } from '@/api/http';
import type { Tokens, User } from '@/api/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useAuthStore } from '@/store/auth.store';
import { roleHome } from '@/hooks/useRoleHome';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(4)
});

type FormData = z.infer<typeof schema>;

export const LoginPage = () => {
  const navigate = useNavigate();
  const setSession = useAuthStore((s) => s.setSession);
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<FormData>({ resolver: zodResolver(schema) });

  const loginMutation = useMutation({
    mutationFn: async (values: FormData) => {
      const tokens = (await http.post<Tokens>(endpoints.auth.login, values))
        .data;
      setSession({
        accessToken: tokens.access_token,
        refreshToken: tokens.refresh_token
      });
      const me = (await http.get<User>(endpoints.users.me)).data;
      setSession({
        accessToken: tokens.access_token,
        refreshToken: tokens.refresh_token,
        user: me
      });
      return me;
    },
    onSuccess: (user) => navigate(roleHome(user.role), { replace: true })
  });

  return (
    <form
      className="space-y-4"
      onSubmit={handleSubmit((values) => loginMutation.mutate(values))}
    >
      <h1 className="text-2xl font-semibold">Sign in</h1>
      <p className="text-sm text-muted-foreground">
        Use role credentials to access dedicated workspace.
      </p>
      <div>
        <Input placeholder="Email" {...register('email')} />
        {errors.email && (
          <p className="mt-1 text-xs text-destructive">
            {errors.email.message}
          </p>
        )}
      </div>
      <div>
        <Input
          type="password"
          placeholder="Password"
          {...register('password')}
        />
        {errors.password && (
          <p className="mt-1 text-xs text-destructive">
            {errors.password.message}
          </p>
        )}
      </div>
      <Button
        className="w-full"
        type="submit"
        disabled={loginMutation.isPending}
      >
        {loginMutation.isPending ? 'Signing in...' : 'Sign in'}
      </Button>
      <p className="text-center text-sm text-muted-foreground">
        Нет аккаунта?{' '}
        <Link
          className="font-medium text-primary underline-offset-4 hover:underline"
          to="/auth/register"
        >
          Зарегистрироваться
        </Link>
      </p>
    </form>
  );
};
