"""Minimal seed data for CoinCraft application."""

import asyncio
from database import create_db_and_tables


async def seed_data():
    """Create database tables only - no dummy data."""
    print("Creating database tables...")
    await create_db_and_tables()
    print("Database tables created successfully!")
    print("No dummy users or data created.")
    print("You can now register new users through the application.")


if __name__ == "__main__":
    asyncio.run(seed_data())