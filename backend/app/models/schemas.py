from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.models.database import TransactionStatus, CorrectionType


# Base Models
class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    model_config = ConfigDict(from_attributes=True)


# User Schemas
class UserBase(BaseSchema):
    """Base user schema."""
    email: EmailStr
    timezone: str = "UTC"


class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseSchema):
    """User login schema."""
    email: EmailStr
    password: str


class UserUpdate(BaseSchema):
    """User update schema."""
    timezone: Optional[str] = None


class UserResponse(UserBase):
    """User response schema."""
    id: UUID
    is_active: bool
    is_verified: bool
    created_at: datetime


# Auth Schemas
class Token(BaseSchema):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenRefresh(BaseSchema):
    """Token refresh schema."""
    refresh_token: str


# Category Schemas
class CategoryBase(BaseSchema):
    """Base category schema."""
    name: str = Field(..., min_length=1, max_length=100)
    color: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    icon: str = Field(..., min_length=1, max_length=10)
    monthly_budget: Optional[Decimal] = Field(None, ge=0)


class CategoryCreate(CategoryBase):
    """Category creation schema."""
    pass


class CategoryUpdate(BaseSchema):
    """Category update schema."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(None, min_length=1, max_length=10)
    monthly_budget: Optional[Decimal] = Field(None, ge=0)


class CategoryResponse(CategoryBase):
    """Category response schema."""
    id: UUID
    user_id: Optional[UUID]
    is_global: bool
    created_at: datetime
    transaction_count: Optional[int] = 0


# Transaction Schemas
class TransactionBase(BaseSchema):
    """Base transaction schema."""
    amount: Decimal = Field(..., gt=0)
    date: date
    vendor: str = Field(..., min_length=1, max_length=255)
    category_id: UUID


class TransactionCreate(TransactionBase):
    """Transaction creation schema."""
    raw_text: Optional[str] = None
    image_url: Optional[str] = None
    parsed_json: Optional[dict] = None


class TransactionUpdate(BaseSchema):
    """Transaction update schema."""
    amount: Optional[Decimal] = Field(None, gt=0)
    date: Optional[date] = None
    vendor: Optional[str] = Field(None, min_length=1, max_length=255)
    category_id: Optional[UUID] = None


class TransactionConfirm(BaseSchema):
    """Transaction confirmation schema."""
    category_id: UUID
    vendor: str = Field(..., min_length=1, max_length=255)
    amount: Decimal = Field(..., gt=0)
    date: date
    remember_vendor: bool = False


class TransactionResponse(TransactionBase):
    """Transaction response schema."""
    id: UUID
    user_id: UUID
    raw_text: Optional[str]
    image_url: Optional[str]
    parsed_json: Optional[dict]
    confidence_score: Optional[int]
    status: TransactionStatus
    created_at: datetime
    updated_at: datetime


class TransactionList(BaseSchema):
    """Transaction list response schema."""
    transactions: List[TransactionResponse]
    total: int
    has_more: bool


# Transaction Processing Schemas
class TransactionUploadResponse(BaseSchema):
    """Transaction upload response schema."""
    transaction_id: UUID
    status: str
    message: str = "Receipt uploaded successfully. Processing started."


class TransactionStatusResponse(BaseSchema):
    """Transaction status response schema."""
    status: TransactionStatus
    progress_percentage: int
    estimated_time_remaining: Optional[int]
    message: str


# Budget Schemas
class BudgetCreate(BaseSchema):
    """Budget creation schema."""
    amount: Decimal = Field(..., gt=0)
    month: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}$")


class BudgetResponse(BaseSchema):
    """Budget response schema."""
    category_id: UUID
    category_name: str
    amount: Decimal
    month: str
    spent: Decimal
    remaining: Decimal
    percentage_used: float


class BudgetHistory(BaseSchema):
    """Budget history response schema."""
    month: str
    categories: List[BudgetResponse]


# Dashboard Schemas
class CategorySpending(BaseSchema):
    """Category spending schema."""
    category_id: UUID
    category_name: str
    amount_spent: Decimal
    budget_amount: Optional[Decimal]
    percentage: float


class TopVendor(BaseSchema):
    """Top vendor schema."""
    vendor: str
    amount: Decimal
    count: int


class DashboardSummary(BaseSchema):
    """Dashboard summary response schema."""
    total_expenses: Decimal
    total_income: Decimal
    savings: Decimal
    budget_remaining: Decimal
    categories_spending: List[CategorySpending]
    top_vendors: List[TopVendor]
    transaction_count: int
    month: str


class ChartDataPoint(BaseSchema):
    """Chart data point schema."""
    month: str
    amount: Decimal


class CategoryChartData(BaseSchema):
    """Category chart data schema."""
    category_id: UUID
    category_name: str
    total_amount: Decimal
    color: str
    monthly_data: List[ChartDataPoint]


class CategoryChartResponse(BaseSchema):
    """Category chart response schema."""
    monthly_data: List[dict]
    totals: List[CategoryChartData]


# Vendor Mapping Schemas
class VendorMappingCreate(BaseSchema):
    """Vendor mapping creation schema."""
    vendor_name: str = Field(..., min_length=1, max_length=255)
    category_id: UUID


class VendorMappingResponse(BaseSchema):
    """Vendor mapping response schema."""
    id: UUID
    vendor_name: str
    category_id: UUID
    category_name: str
    confidence: int
    usage_count: int
    created_at: datetime


# Audit Schemas
class AuditCorrectionResponse(BaseSchema):
    """Audit correction response schema."""
    id: UUID
    transaction_id: UUID
    old_category_name: Optional[str]
    new_category_name: str
    old_vendor: Optional[str]
    new_vendor: Optional[str]
    old_amount: Optional[Decimal]
    new_amount: Optional[Decimal]
    correction_type: CorrectionType
    created_at: datetime


# Error Schemas
class ErrorResponse(BaseSchema):
    """Error response schema."""
    error: str
    message: str
    details: Optional[dict] = None


class ValidationError(BaseSchema):
    """Validation error schema."""
    field: str
    message: str


class ValidationErrorResponse(BaseSchema):
    """Validation error response schema."""
    error: str = "Validation Error"
    message: str = "Invalid input data"
    details: List[ValidationError]


# Health Check Schemas
class HealthCheck(BaseSchema):
    """Health check response schema."""
    status: str
    version: str
    timestamp: datetime
    services: dict


# File Upload Schemas
class FileUploadResponse(BaseSchema):
    """File upload response schema."""
    file_url: str
    file_name: str
    file_size: int
    content_type: str