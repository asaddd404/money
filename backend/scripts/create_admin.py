#!/usr/bin/env python3
from __future__ import annotations
"""Create initial admin user in DB.

Usage:
  cd backend
  python scripts/create_admin.py --email admin@example.com --password 'StrongPass123!' --full-name 'Main Admin' --center-id 1
"""

import argparse
import asyncio
import sys
from pathlib import Path
from urllib.parse import urlparse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.core.config import get_settings
from app.core.security import hash_password
from app.models.center import Center
from app.models.user import User, UserRole


def _local_fallback_database_url(db_url: str) -> str:
    parsed = urlparse(db_url)
    if parsed.hostname == 'db':
        # `db` host is valid inside docker-compose network only.
        return db_url.replace('@db:', '@localhost:')
    return db_url


async def _create_admin(
    session: AsyncSession,
    email: str,
    password: str,
    full_name: str,
    center_id: int,
) -> None:
    center = await session.get(Center, center_id)
    if not center:
        raise RuntimeError(f'Center with id={center_id} not found. Create center first (or use bootstrap-admin API).')

    existing = await session.scalar(select(User).where(User.email == email))
    if existing:
        raise RuntimeError(f'User with email={email} already exists.')

    user = User(
        center_id=center_id,
        email=email,
        password_hash=hash_password(password),
        full_name=full_name,
        role=UserRole.admin,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    print(f'Created admin user id={user.id}, email={user.email}, center_id={user.center_id}')


async def main() -> None:
    parser = argparse.ArgumentParser(description='Create admin user for Coins backend')
    parser.add_argument('--email', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--full-name', required=True)
    parser.add_argument('--center-id', required=True, type=int)
    parser.add_argument('--database-url', default=None, help='Optional DB URL override')
    args = parser.parse_args()

    settings = get_settings()
    db_url = args.database_url or settings.database_url
    tried_fallback = False

    for candidate_url in [db_url, _local_fallback_database_url(db_url)]:
        if candidate_url == db_url and tried_fallback:
            continue
        engine = create_async_engine(candidate_url, future=True)
        session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
        try:
            async with session_factory() as session:
                await _create_admin(session, args.email, args.password, args.full_name, args.center_id)
            await engine.dispose()
            return
        except Exception as exc:
            await engine.dispose()
            if candidate_url != db_url:
                raise
            if '@db:' in db_url:
                tried_fallback = True
                continue
            raise exc


if __name__ == '__main__':
    asyncio.run(main())

from sqlalchemy import select

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User, UserRole


async def create_admin(email: str, password: str, full_name: str, center_id: int) -> None:
    async with SessionLocal() as session:
        exists = await session.execute(select(User).where(User.email == email))
        if exists.scalar_one_or_none():
            print(f'User with email={email} already exists')
            return

        user = User(
            email=email,
            password_hash=hash_password(password),
            full_name=full_name,
            center_id=center_id,
            role=UserRole.admin,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        print(f'Admin created: id={user.id}, email={user.email}, center_id={user.center_id}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--full-name', required=True)
    parser.add_argument('--center-id', type=int, default=1)
    args = parser.parse_args()

    asyncio.run(create_admin(args.email, args.password, args.full_name, args.center_id))
