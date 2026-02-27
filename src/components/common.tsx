import type React from 'react';
import { Search } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { formatCoins } from '@/utils/format';

export const PageHeader = ({
  title,
  actions
}: {
  title: string;
  actions?: React.ReactNode;
}) => (
  <div className="mb-4 flex items-center justify-between gap-3">
    <h1 className="text-xl font-semibold">{title}</h1>
    <div>{actions}</div>
  </div>
);

export const CoinsAmount = ({ amount }: { amount: number }) => (
  <span className="font-semibold">🪙 {formatCoins(amount)}</span>
);

export const PeriodPicker = ({
  value,
  onChange
}: {
  value: string;
  onChange: (v: string) => void;
}) => (
  <div className="grid grid-cols-3 gap-2">
    {['day', 'week', 'month'].map((period) => (
      <button
        key={period}
        onClick={() => onChange(period)}
        className={`min-h-11 rounded-md border capitalize ${value === period ? 'bg-primary text-primary-foreground' : ''}`}
      >
        {period}
      </button>
    ))}
  </div>
);

export const SearchInput = ({
  value,
  onChange
}: {
  value: string;
  onChange: (v: string) => void;
}) => (
  <div className="relative">
    <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
    <Input
      className="pl-9"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder="Search"
    />
  </div>
);
