"""initial

Revision ID: e4d5ccc6ec42
Revises:
Create Date: 2024-06-11 10:43:07.012126

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'e4d5ccc6ec42'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'roles',
        sa.Column('title', sa.TEXT(), nullable=False),
        sa.Column('description', sa.TEXT(), nullable=True),
        sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created_by', sa.TEXT(), nullable=True),
        sa.Column(
            'created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False
        ),
        sa.Column('updated_by', sa.TEXT(), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('title'),
    )
    op.create_table(
        'users',
        sa.Column('username', sa.TEXT(), nullable=False),
        sa.Column('email', sa.TEXT(), nullable=False),
        sa.Column('hashed_password', sa.TEXT(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created_by', sa.TEXT(), nullable=True),
        sa.Column(
            'created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False
        ),
        sa.Column('updated_by', sa.TEXT(), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
    )
    op.create_table(
        'history',
        sa.Column('user_agent', sa.TEXT(), nullable=False),
        sa.Column('login_type', sa.TEXT(), nullable=False),
        sa.Column('session_id', sa.Uuid(), nullable=False),
        sa.Column('auth_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created_by', sa.TEXT(), nullable=True),
        sa.Column(
            'created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False
        ),
        sa.Column('updated_by', sa.TEXT(), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'user_role_associations',
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('role_id', sa.Uuid(), nullable=False),
        sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created_by', sa.TEXT(), nullable=True),
        sa.Column(
            'created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False
        ),
        sa.Column('updated_by', sa.TEXT(), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ['role_id'],
            ['roles.id'],
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'role_id', name='user_role_association_unique'),
    )


def downgrade() -> None:
    op.drop_table('user_role_associations')
    op.drop_table('history')
    op.drop_table('users')
    op.drop_table('roles')
