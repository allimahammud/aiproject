"""create users and items tables

Revision ID: 001
Revises: 
Create Date: 2025-11-28
"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('password_hash', sa.String, nullable=False),
        sa.Column('role', sa.String, nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=True, default=True),
    )
    op.create_table(
        'items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id'), nullable=True),
    )

def downgrade():
    op.drop_table('items')
    op.drop_table('users')
