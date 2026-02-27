import { useMemo, useState } from 'react';
import { debounce } from '@/utils/format';

export const useDebouncedSearch = () => {
  const [value, setValue] = useState('');
  const [query, setQuery] = useState('');
  const onDebounce = useMemo(
    () => debounce((next: string) => setQuery(next)),
    []
  );
  const onChange = (next: string) => {
    setValue(next);
    onDebounce(next);
  };
  return { value, query, onChange };
};
