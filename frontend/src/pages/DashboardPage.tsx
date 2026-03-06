import { useEffect, useState } from 'react';
import { getMe } from '../api/auth';
import { getGlobalLeaderboard, getGroups, getProducts } from '../api/resources';
import type { Group, LeaderboardRow, Product, UserMe } from '../types/api';

export function DashboardPage() {
  const [user, setUser] = useState<UserMe | null>(null);
  const [groups, setGroups] = useState<Group[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [leaderboard, setLeaderboard] = useState<LeaderboardRow[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      setError(null);
      try {
        const [me, groupsData, productsData, leaderboardData] = await Promise.all([
          getMe(),
          getGroups(),
          getProducts(),
          getGlobalLeaderboard('week'),
        ]);
        setUser(me);
        setGroups(groupsData);
        setProducts(productsData);
        setLeaderboard(leaderboardData);
      } catch {
        setError('Failed to load dashboard. Please login first.');
      }
    }

    load();
  }, []);

  return (
    <div>
      <h1>Coins Platform Dashboard</h1>
      {error && <p style={{ color: 'crimson' }}>{error}</p>}
      {user && (
        <p>
          Signed in as <b>{user.full_name}</b> ({user.role})
        </p>
      )}

      <section>
        <h2>Groups ({groups.length})</h2>
        <ul>
          {groups.map((group) => (
            <li key={group.id}>
              #{group.id} {group.name}
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Products ({products.length})</h2>
        <ul>
          {products.map((product) => (
            <li key={product.id}>
              {product.name} — {product.price} coins — stock {product.stock}
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Global Leaderboard (week)</h2>
        <ol>
          {leaderboard.map((row) => (
            <li key={row.student_id}>
              Student {row.student_id}: {row.score}
            </li>
          ))}
        </ol>
      </section>
    </div>
  );
}
