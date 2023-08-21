"""Add created_at column

Revision ID: 0002
Revises: 0001
Create Date: 2022-09-07 16:32:52.136057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('datastores', sa.Column('created_at', sa.DateTime))


def downgrade():
    op.drop_column('datastores', 'created_at')
