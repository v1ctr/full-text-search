"""Initial migration.

Revision ID: e2d73cd9f007
Revises: 
Create Date: 2020-10-23 22:50:49.101636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2d73cd9f007'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=10), nullable=True),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('director', sa.Text(), nullable=True),
    sa.Column('actors', sa.Text(), nullable=True),
    sa.Column('country', sa.Text(), nullable=True),
    sa.Column('date_added', sa.Date(), nullable=True),
    sa.Column('release_year', sa.Integer(), nullable=True),
    sa.Column('rating', sa.String(length=10), nullable=True),
    sa.Column('duration', sa.String(length=10), nullable=True),
    sa.Column('listed_in', sa.Text(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('show')
    # ### end Alembic commands ###
