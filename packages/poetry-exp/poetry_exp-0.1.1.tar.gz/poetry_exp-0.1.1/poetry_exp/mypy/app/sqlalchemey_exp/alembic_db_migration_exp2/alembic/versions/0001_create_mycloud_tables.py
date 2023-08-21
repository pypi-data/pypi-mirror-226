"""Create_mycloud_tables

Revision ID: 0001
Revises: 
Create Date: 2022-09-07 16:23:48.206558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'datastores',
        # sa.Column('id', sa.Integer, primary_key=True),
        # if you add primary key it will add one seq datastores_id_seq
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )


def downgrade():
    op.drop_table('datastores')
