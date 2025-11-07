import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Decimal as SQLDecimal,
    Enum,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
    select,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base


class User(Base):
    """User model for authentication and user data."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    categories: Mapped[list["Category"]] = relationship(
        "Category", back_populates="user", cascade="all, delete-orphan"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="user", cascade="all, delete-orphan"
    )
    budgets_history: Mapped[list["BudgetsHistory"]] = relationship(
        "BudgetsHistory", back_populates="user", cascade="all, delete-orphan"
    )
    vendor_mappings: Mapped[list["VendorMapping"]] = relationship(
        "VendorMapping", back_populates="user", cascade="all, delete-orphan"
    )
    audit_corrections: Mapped[list["AuditCorrection"]] = relationship(
        "AuditCorrection", back_populates="user", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("idx_user_email", "email"),)

    # Class methods for database operations
    @classmethod
    async def get_by_id(cls, db: AsyncSession, user_id: uuid.UUID) -> Optional["User"]:
        """Get user by ID."""
        result = await db.execute(select(cls).where(cls.id == user_id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_by_email(cls, db: AsyncSession, email: str) -> Optional["User"]:
        """Get user by email."""
        result = await db.execute(select(cls).where(cls.email == email))
        return result.scalar_one_or_none()

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs) -> "User":
        """Create new user."""
        user = cls(**kwargs)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


class Category(Base):
    """Transaction categories model."""

    __tablename__ = "categories"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    color: Mapped[str] = mapped_column(String(7), nullable=False)  # Hex color
    icon: Mapped[str] = mapped_column(String(10), nullable=False)  # Emoji
    monthly_budget: Mapped[Optional[Decimal]] = mapped_column(
        SQLDecimal(precision=10, scale=2), nullable=True
    )
    is_global: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="categories")
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="category"
    )
    budgets_history: Mapped[list["BudgetsHistory"]] = relationship(
        "BudgetsHistory", back_populates="category"
    )
    vendor_mappings: Mapped[list["VendorMapping"]] = relationship(
        "VendorMapping", back_populates="category"
    )
    audit_corrections: Mapped[list["AuditCorrection"]] = relationship(
        "AuditCorrection", back_populates="new_category"
    )

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="unique_category_name_per_user"),
        Index("idx_category_user", "user_id"),
    )


class TransactionStatus(str, Enum):
    """Transaction processing status."""
    PROCESSING = "processing"
    PARSED = "parsed"
    CLASSIFIED = "classified"
    CONFIRMED = "confirmed"
    CORRECTED = "corrected"
    ERROR = "error"


class Transaction(Base):
    """Transaction model for expense records."""

    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    category_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(
        SQLDecimal(precision=10, scale=2), nullable=False
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    vendor: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    raw_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    parsed_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    confidence_score: Mapped[Optional[float]] = mapped_column(
        Integer, nullable=True
    )  # ML confidence percentage
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus), default=TransactionStatus.PROCESSING
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="transactions")
    category: Mapped["Category"] = relationship("Category", back_populates="transactions")
    audit_corrections: Mapped[list["AuditCorrection"]] = relationship(
        "AuditCorrection", back_populates="transaction", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_transaction_user_date", "user_id", "date"),
        Index("idx_transaction_vendor", "vendor"),
        Index("idx_transaction_status", "status"),
    )


class BudgetsHistory(Base):
    """Budget history tracking model."""

    __tablename__ = "budgets_history"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    category_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False
    )
    month: Mapped[str] = mapped_column(String(7), nullable=False)  # YYYY-MM format
    budget_amount: Mapped[Decimal] = mapped_column(
        SQLDecimal(precision=10, scale=2), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="budgets_history")
    category: Mapped["Category"] = relationship(
        "Category", back_populates="budgets_history"
    )

    __table_args__ = (
        UniqueConstraint("user_id", "category_id", "month", name="unique_budget_per_month"),
        Index("idx_budget_user_month", "user_id", "month"),
    )


class VendorMapping(Base):
    """Vendor to category mapping for learning."""

    __tablename__ = "vendor_mappings"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    vendor_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    category_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False
    )
    confidence: Mapped[int] = mapped_column(Integer, default=80)  # 0-100 percentage
    usage_count: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="vendor_mappings")
    category: Mapped["Category"] = relationship(
        "Category", back_populates="vendor_mappings"
    )

    __table_args__ = (
        UniqueConstraint("user_id", "vendor_name", name="unique_vendor_per_user"),
        Index("idx_vendor_mapping_user", "user_id"),
        Index("idx_vendor_mapping_name", "vendor_name"),
    )


class CorrectionType(str, Enum):
    """Types of corrections users can make."""
    CATEGORY = "category"
    VENDOR = "vendor"
    AMOUNT = "amount"
    ALL = "all"


class AuditCorrection(Base):
    """Audit trail for user corrections (active learning data)."""

    __tablename__ = "audit_corrections"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    transaction_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("transactions.id"), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    old_category_id: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True
    )
    new_category_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False
    )
    old_vendor: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    new_vendor: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    old_amount: Mapped[Optional[Decimal]] = mapped_column(
        SQLDecimal(precision=10, scale=2), nullable=True
    )
    new_amount: Mapped[Optional[Decimal]] = mapped_column(
        SQLDecimal(precision=10, scale=2), nullable=True
    )
    correction_type: Mapped[CorrectionType] = mapped_column(
        Enum(CorrectionType), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    transaction: Mapped["Transaction"] = relationship(
        "Transaction", back_populates="audit_corrections"
    )
    user: Mapped["User"] = relationship("User", back_populates="audit_corrections")
    new_category: Mapped["Category"] = relationship(
        "Category", back_populates="audit_corrections"
    )

    __table_args__ = (
        Index("idx_audit_transaction", "transaction_id"),
        Index("idx_audit_user", "user_id"),
        Index("idx_audit_correction_type", "correction_type"),
    )