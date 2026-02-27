import { cn } from '@/utils/cn';
import type { HTMLAttributes } from 'react';

export const Card = ({ className, ...props }: HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('rounded-xl border bg-card p-4 shadow-sm', className)} {...props} />
);
