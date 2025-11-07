from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.database import User
from app.models.schemas import (
    BudgetResponse,
    BudgetCreate,
    BudgetHistory,
)
from app.api.v1.dependencies import get_current_active_user

router = APIRouter()


@router.post("/{category_id}", response_model=BudgetResponse)
async def set_budget(
    category_id: UUID,
    budget_data: BudgetCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Set or update budget for a category."""
    # TODO: Implement budget creation/update
    # 1. Validate category ownership
    # 2. Create or update budget record
    pass


@router.get("/{category_id}/current", response_model=BudgetResponse)
async def get_current_budget(
    category_id: UUID,
    month: str = None,  # YYYY-MM format
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get current budget for category."""
    # TODO: Implement current budget retrieval with spending calculation
    pass


@router.get("/history", response_model=List[BudgetHistory])
async def get_budget_history(
    months_count: int = 12,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get budget history for all categories."""
    # TODO: Implement budget history retrieval
    return []


@router.get("/summary")
async def get_budgets_summary(
    month: str = None,  # YYYY-MM format
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get budget summary for all categories."""
    # TODO: Implement budget summary with total vs spent
    pass