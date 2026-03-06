"""Create initial admin user in DB.

Usage:
  cd backend
  python scripts/create_admin.py --email admin@example.com --password 'StrongPass123!' --full-name 'Main Admin' --center-id 1
"""

import argparse
import asyncio
import sys
from pathlib import Path

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
