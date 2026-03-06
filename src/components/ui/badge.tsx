import { cn } from '@/utils/cn';
import type { HTMLAttributes } from 'react';

export const Badge = ({
  className,
  ...props
}: HTMLAttributes<HTMLSpanElement>) => (
  <span
    className={cn(
      'inline-flex items-center rounded-full bg-muted px-2.5 py-1 text-xs font-semibold',
      className
    )}
    {...props}
  />
);
