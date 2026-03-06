import * as Dialog from '@radix-ui/react-dialog';
import { X } from 'lucide-react';
import { cn } from '@/utils/cn';

export const Sheet = Dialog.Root;
export const SheetTrigger = Dialog.Trigger;
export const SheetClose = Dialog.Close;

export const SheetContent = ({
  className,
  ...props
}: Dialog.DialogContentProps) => (
  <Dialog.Portal>
    <Dialog.Overlay className="fixed inset-0 bg-black/40" />
    <Dialog.Content
      className={cn(
        'fixed bottom-0 left-0 right-0 z-50 rounded-t-2xl border bg-background p-4',
        className
      )}
      {...props}
    >
      <Dialog.Close className="absolute right-4 top-4">
        <X className="size-4" />
      </Dialog.Close>
      {props.children}
    </Dialog.Content>
  </Dialog.Portal>
);
