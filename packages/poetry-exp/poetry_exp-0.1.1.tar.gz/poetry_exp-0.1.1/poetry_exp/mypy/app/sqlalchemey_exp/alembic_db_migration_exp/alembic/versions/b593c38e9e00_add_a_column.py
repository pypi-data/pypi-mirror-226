"""Add a column

Revision ID: b593c38e9e00
Revises: cf6f24cd8d39
Create Date: 2022-09-07 16:14:26.776513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b593c38e9e00'
down_revision = 'cf6f24cd8d39'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))


def downgrade():
    op.drop_column('account', 'last_transaction_date')
