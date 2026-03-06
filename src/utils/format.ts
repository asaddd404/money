export const formatCoins = (value: number) =>
  new Intl.NumberFormat('en-US').format(value);

export const debounce = <TArgs extends unknown[]>(
  fn: (...args: TArgs) => void,
  delay = 400
) => {
  let id: ReturnType<typeof setTimeout>;
  return (...args: TArgs) => {
    clearTimeout(id);
    id = setTimeout(() => fn(...args), delay);
  };
};
