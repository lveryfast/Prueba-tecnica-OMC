"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2026-04-24

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_extension('uuid-ossp', if_not_exists=True)
    
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('nombre', sa.String(length=255), nullable=False),
        sa.Column('rol', sa.String(length=50), server_default='user', nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('idx_users_email', 'users', ['email'], unique=False)
    op.create_index('idx_users_rol', 'users', ['rol'], unique=False)
    
    op.create_table(
        'leads',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('nombre', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('telefono', sa.String(length=50), nullable=True),
        sa.Column('fuente', sa.String(length=50), nullable=False),
        sa.Column('producto_interes', sa.String(length=255), nullable=True),
        sa.Column('presupuesto', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), server_default='false', nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('idx_leads_email', 'leads', ['email'], unique=False)
    op.create_index('idx_leads_fuente', 'leads', ['fuente'], unique=False)
    op.create_index('idx_leads_created_at', 'leads', ['created_at'], unique=False)
    op.create_index('idx_leads_is_deleted', 'leads', ['is_deleted'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_leads_is_deleted', table_name='leads')
    op.drop_index('idx_leads_created_at', table_name='leads')
    op.drop_index('idx_leads_fuente', table_name='leads')
    op.drop_index('idx_leads_email', table_name='leads')
    op.drop_table('leads')
    op.drop_index('idx_users_rol', table_name='users')
    op.drop_index('idx_users_email', table_name='users')
    op.drop_table('users')