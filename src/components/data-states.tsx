import { AlertTriangle, Inbox } from 'lucide-react';

export const LoadingSkeleton = () => <div className="space-y-3">{Array.from({ length: 3 }).map((_, i) => <div key={i} className="h-24 animate-pulse rounded-xl bg-muted" />)}</div>;

export const EmptyState = ({ title, description }: { title: string; description: string }) => (
  <div className="rounded-xl border border-dashed p-6 text-center">
    <Inbox className="mx-auto mb-2 size-7 text-muted-foreground" />
    <p className="font-medium">{title}</p>
    <p className="text-sm text-muted-foreground">{description}</p>
  </div>
);

export const ErrorState = ({ message, details }: { message: string; details?: Record<string, unknown> }) => (
  <div className="rounded-xl border border-destructive/40 bg-destructive/10 p-4">
    <div className="flex items-center gap-2 font-medium"><AlertTriangle className="size-4" /> {message}</div>
    {details && (
      <details className="mt-2 text-xs">
        <summary>Details</summary>
        <pre className="mt-2 overflow-auto rounded bg-background p-2">{JSON.stringify(details, null, 2)}</pre>
      </details>
    )}
  </div>
);
