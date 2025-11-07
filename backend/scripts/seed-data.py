#!/usr/bin/env python3
"""
Seed data script for expense manager application.

This script creates initial system categories and sample data for development.
"""

import asyncio
import uuid
from decimal import Decimal
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal, init_db
from app.models.database import Category, User


# System categories as specified in planning document
SYSTEM_CATEGORIES = [
    {
        "name": "Food & Dining",
        "icon": "🍔",
        "color": "#FF6B6B",
        "description": "Restaurants, cafes, bars, food delivery"
    },
    {
        "name": "Groceries",
        "icon": "🛒",
        "color": "#4ECDC4",
        "description": "Supermarkets, food stores, farmers markets"
    },
    {
        "name": "Transportation",
        "icon": "🚗",
        "color": "#45B7D1",
        "description": "Uber, fuel, public transport, parking"
    },
    {
        "name": "Utilities",
        "icon": "💡",
        "color": "#96CEB4",
        "description": "Electricity, water, internet, phone bills"
    },
    {
        "name": "Housing",
        "icon": "🏠",
        "color": "#DDA0DD",
        "description": "Rent, maintenance, home supplies"
    },
    {
        "name": "Healthcare",
        "icon": "🏥",
        "color": "#FFB6C1",
        "description": "Hospitals, pharmacies, insurance, doctors"
    },
    {
        "name": "Entertainment",
        "icon": "🎬",
        "color": "#FFD93D",
        "description": "Movies, games, subscriptions, events"
    },
    {
        "name": "Shopping",
        "icon": "🛍️",
        "color": "#6C5CE7",
        "description": "Clothing, electronics, books, general shopping"
    },
    {
        "name": "Education",
        "icon": "📚",
        "color": "#74B9FF",
        "description": "Courses, books, training, school supplies"
    },
    {
        "name": "Other",
        "icon": "📌",
        "color": "#A8A8A8",
        "description": "Miscellaneous expenses"
    }
]


async def create_system_categories():
    """Create system categories."""
    async with AsyncSessionLocal() as db:
        print("Creating system categories...")

        for cat_data in SYSTEM_CATEGORIES:
            # Check if category already exists
            existing = await db.execute(
                select(Category).where(
                    Category.name == cat_data["name"],
                    Category.is_global == True
                )
            )
            if existing.scalar_one_or_none():
                print(f"Category '{cat_data['name']}' already exists, skipping...")
                continue

            category = Category(
                name=cat_data["name"],
                icon=cat_data["icon"],
                color=cat_data["color"],
                is_global=True,
                user_id=None,  # Global categories have no user
            )

            db.add(category)
            print(f"Created category: {cat_data['name']} {cat_data['icon']}")

        await db.commit()
        print("System categories created successfully!")


async def create_demo_user():
    """Create a demo user for testing."""
    async with AsyncSessionLocal() as db:
        print("Creating demo user...")

        # Check if demo user already exists
        existing = await User.get_by_email(db, "demo@example.com")
        if existing:
            print("Demo user already exists, skipping...")
            return existing

        # In a real app, you'd hash the password
        from app.core.security import get_password_hash

        user = User(
            email="demo@example.com",
            password_hash=get_password_hash("demo123"),
            timezone="UTC",
            is_active=True,
            is_verified=True,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        print(f"Created demo user: {user.email}")
        return user


async def create_sample_transactions():
    """Create sample transactions for demo user."""
    async with AsyncSessionLocal() as db:
        print("Creating sample transactions...")

        # Get demo user
        demo_user = await User.get_by_email(db, "demo@example.com")
        if not demo_user:
            print("Demo user not found, creating first...")
            demo_user = await create_demo_user()

        # Get some categories
        food_category = await db.execute(
            select(Category).where(Category.name == "Food & Dining")
        )
        food_cat = food_category.scalar_one_or_none()

        transport_category = await db.execute(
            select(Category).where(Category.name == "Transportation")
        )
        transport_cat = transport_category.scalar_one_or_none()

        if not food_cat or not transport_cat:
            print("Required categories not found, skipping sample transactions...")
            return

        # TODO: Create sample transactions when the Transaction model is fully implemented
        print("Sample transactions creation will be implemented when Transaction model is complete")


async def main():
    """Main seeding function."""
    print("🌱 Starting database seeding...")

    try:
        # Initialize database
        await init_db()
        print("Database initialized")

        # Create system categories
        await create_system_categories()

        # Create demo user and sample data
        await create_demo_user()
        await create_sample_transactions()

        print("✅ Database seeding completed successfully!")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        raise


if __name__ == "__main__":
    # Import here to avoid circular imports
    from sqlalchemy import select

    asyncio.run(main())