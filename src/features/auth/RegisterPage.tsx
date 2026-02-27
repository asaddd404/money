import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { z } from 'zod';
import { endpoints } from '@/api/endpoints';
import { http } from '@/api/http';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

const schema = z.object({
  full_name: z.string().min(2, 'Введите имя'),
  email: z.string().email('Неверный email'),
  password: z.string().min(8, 'Минимум 8 символов'),
  center_id: z.coerce.number().int().positive('Укажите center_id')
});

type RegisterForm = z.infer<typeof schema>;

export const RegisterPage = () => {
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<RegisterForm>({
    resolver: zodResolver(schema),
    defaultValues: { center_id: 1 }
  });

  const registerMutation = useMutation({
    mutationFn: (payload: RegisterForm) =>
      http.post(endpoints.auth.registerStudent, payload),
    onSuccess: () => navigate('/auth/login', { replace: true })
  });

  return (
    <form
      className="space-y-4"
      onSubmit={handleSubmit((values) => registerMutation.mutate(values))}
    >
      <h1 className="text-2xl font-semibold">Регистрация студента</h1>
      <p className="text-sm text-muted-foreground">
        После регистрации войдите в аккаунт на странице логина.
      </p>

      <div>
        <Input placeholder="Имя и фамилия" {...register('full_name')} />
        {errors.full_name && (
          <p className="mt-1 text-xs text-destructive">
            {errors.full_name.message}
          </p>
        )}
      </div>

      <div>
        <Input placeholder="Email" {...register('email')} />
        {errors.email && (
          <p className="mt-1 text-xs text-destructive">
            {errors.email.message}
          </p>
        )}
      </div>

      <div>
        <Input type="password" placeholder="Пароль" {...register('password')} />
        {errors.password && (
          <p className="mt-1 text-xs text-destructive">
            {errors.password.message}
          </p>
        )}
      </div>

      <div>
        <Input
          type="number"
          placeholder="Center ID"
          {...register('center_id')}
        />
        {errors.center_id && (
          <p className="mt-1 text-xs text-destructive">
            {errors.center_id.message}
          </p>
        )}
      </div>

      <Button
        className="w-full"
        type="submit"
        disabled={registerMutation.isPending}
      >
        {registerMutation.isPending
          ? 'Создаем аккаунт...'
          : 'Зарегистрироваться'}
      </Button>

      <p className="text-center text-sm text-muted-foreground">
        Уже есть аккаунт?{' '}
        <Link
          className="font-medium text-primary underline-offset-4 hover:underline"
          to="/auth/login"
        >
          Войти
        </Link>
      </p>
    </form>
  );
};
