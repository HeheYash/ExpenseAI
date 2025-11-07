from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    transactions,
    categories,
    budgets,
    dashboard,
    users,
)

api_router = APIRouter()

# Auth endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Transaction endpoints
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

# Category endpoints
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])

# Budget endpoints
api_router.include_router(budgets.router, prefix="/budgets", tags=["Budgets"])

# Dashboard endpoints
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

# User endpoints
api_router.include_router(users.router, prefix="/users", tags=["Users"])