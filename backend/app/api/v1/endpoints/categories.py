from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.database import User
from app.models.schemas import (
    CategoryResponse,
    CategoryCreate,
    CategoryUpdate,
)
from app.api.v1.dependencies import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    include_global: bool = True,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get user's categories including global categories."""
    # TODO: Implement category listing
    # 1. Get user-specific categories
    # 2. Include global categories if requested
    # 3. Add transaction counts
    return []


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Create new category."""
    # TODO: Implement category creation
    # 1. Validate name uniqueness for user
    # 2. Create category with user_id
    pass


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get specific category."""
    # TODO: Implement category retrieval with ownership check
    pass


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Update category."""
    # TODO: Implement category update with ownership check
    pass


@router.delete("/{category_id}")
async def delete_category(
    category_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Delete category."""
    # TODO: Implement category deletion with ownership check
    # 1. Check if category has transactions
    # 2. Prevent deletion if in use or reassign transactions
    pass