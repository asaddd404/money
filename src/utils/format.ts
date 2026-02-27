export const formatCoins = (value: number) => new Intl.NumberFormat('en-US').format(value);
export const debounce = <T extends (...args: any[]) => void>(fn: T, delay = 400) => {
  let id: ReturnType<typeof setTimeout>;
  return (...args: Parameters<T>) => {
    clearTimeout(id);
    id = setTimeout(() => fn(...args), delay);
  };
};
