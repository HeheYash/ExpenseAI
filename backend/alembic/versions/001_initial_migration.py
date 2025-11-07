"""Initial migration

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, None] = None
depends_on: Union[str, None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('timezone', sa.String(length=50), nullable=True, default='UTC'),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('is_verified', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('idx_user_email', 'users', ['email'], unique=False)

    # Create categories table
    op.create_table('categories',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('color', sa.String(length=7), nullable=False),
        sa.Column('icon', sa.String(length=10), nullable=False),
        sa.Column('monthly_budget', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('is_global', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'name', name='unique_category_name_per_user')
    )
    op.create_index('idx_category_user', 'categories', ['user_id'], unique=False)

    # Create transactions table
    op.create_table('transactions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('vendor', sa.String(length=255), nullable=False),
        sa.Column('raw_text', sa.Text(), nullable=True),
        sa.Column('image_url', sa.String(length=500), nullable=True),
        sa.Column('parsed_json', sa.JSON(), nullable=True),
        sa.Column('confidence_score', sa.Integer(), nullable=True),
        sa.Column('status', sa.Enum('PROCESSING', 'PARSED', 'CLASSIFIED', 'CONFIRMED', 'CORRECTED', 'ERROR', name='transactionstatus'), nullable=True, default='PROCESSING'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_transaction_status', 'transactions', ['status'], unique=False)
    op.create_index('idx_transaction_user_date', 'transactions', ['user_id', 'date'], unique=False)
    op.create_index('idx_transaction_vendor', 'transactions', ['vendor'], unique=False)

    # Create budgets_history table
    op.create_table('budgets_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('month', sa.String(length=7), nullable=False),
        sa.Column('budget_amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'category_id', 'month', name='unique_budget_per_month')
    )
    op.create_index('idx_budget_user_month', 'budgets_history', ['user_id', 'month'], unique=False)

    # Create vendor_mappings table
    op.create_table('vendor_mappings',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('vendor_name', sa.String(length=255), nullable=False),
        sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('confidence', sa.Integer(), nullable=True, default=80),
        sa.Column('usage_count', sa.Integer(), nullable=True, default=1),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'vendor_name', name='unique_vendor_per_user')
    )
    op.create_index('idx_vendor_mapping_name', 'vendor_mappings', ['vendor_name'], unique=False)
    op.create_index('idx_vendor_mapping_user', 'vendor_mappings', ['user_id'], unique=False)

    # Create audit_corrections table
    op.create_table('audit_corrections',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('transaction_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('old_category_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('new_category_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('old_vendor', sa.String(length=255), nullable=True),
        sa.Column('new_vendor', sa.String(length=255), nullable=True),
        sa.Column('old_amount', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('new_amount', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('correction_type', sa.Enum('CATEGORY', 'VENDOR', 'AMOUNT', 'ALL', name='correctiontype'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['new_category_id'], ['categories.id'], ),
        sa.ForeignKeyConstraint(['old_category_id'], ['categories.id'], ),
        sa.ForeignKeyConstraint(['transaction_id'], ['transactions.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_audit_correction_type', 'audit_corrections', ['correction_type'], unique=False)
    op.create_index('idx_audit_transaction', 'audit_corrections', ['transaction_id'], unique=False)
    op.create_index('idx_audit_user', 'audit_corrections', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_audit_user', table_name='audit_corrections')
    op.drop_index('idx_audit_transaction', table_name='audit_corrections')
    op.drop_index('idx_audit_correction_type', table_name='audit_corrections')
    op.drop_table('audit_corrections')
    op.drop_index('idx_vendor_mapping_user', table_name='vendor_mappings')
    op.drop_index('idx_vendor_mapping_name', table_name='vendor_mappings')
    op.drop_table('vendor_mappings')
    op.drop_index('idx_budget_user_month', table_name='budgets_history')
    op.drop_table('budgets_history')
    op.drop_index('idx_transaction_vendor', table_name='transactions')
    op.drop_index('idx_transaction_user_date', table_name='transactions')
    op.drop_index('idx_transaction_status', table_name='transactions')
    op.drop_table('transactions')
    op.drop_index('idx_category_user', table_name='categories')
    op.drop_table('categories')
    op.drop_index('idx_user_email', table_name='users')
    op.drop_table('users')