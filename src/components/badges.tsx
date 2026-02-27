import { Badge } from '@/components/ui/badge';
import type { Role } from '@/api/types';

export const RoleBadge = ({ role }: { role: Role }) => (
  <Badge className="capitalize">{role}</Badge>
);

export const OrderStatusBadge = ({ status }: { status: string }) => {
  const color =
    status === 'approved' || status === 'completed'
      ? 'bg-emerald-500/20'
      : status === 'rejected'
        ? 'bg-destructive/20'
        : '';
  return <Badge className={color}>{status}</Badge>;
};
