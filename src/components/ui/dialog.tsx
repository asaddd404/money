import * as Dialog from '@radix-ui/react-dialog';
import { cn } from '@/utils/cn';

export const ConfirmDialog = ({
  open,
  onOpenChange,
  title,
  description,
  onConfirm
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  description: string;
  onConfirm: () => void;
}) => (
  <Dialog.Root open={open} onOpenChange={onOpenChange}>
    <Dialog.Portal>
      <Dialog.Overlay className="fixed inset-0 bg-black/50" />
      <Dialog.Content className={cn('fixed left-1/2 top-1/2 w-[92vw] max-w-md -translate-x-1/2 -translate-y-1/2 rounded-xl border bg-card p-4')}>
        <Dialog.Title className="font-semibold">{title}</Dialog.Title>
        <Dialog.Description className="mt-2 text-sm text-muted-foreground">{description}</Dialog.Description>
        <div className="mt-4 flex gap-2">
          <button className="min-h-11 flex-1 rounded-md border" onClick={() => onOpenChange(false)}>Cancel</button>
          <button className="min-h-11 flex-1 rounded-md bg-destructive text-destructive-foreground" onClick={onConfirm}>Confirm</button>
        </div>
      </Dialog.Content>
    </Dialog.Portal>
  </Dialog.Root>
);
