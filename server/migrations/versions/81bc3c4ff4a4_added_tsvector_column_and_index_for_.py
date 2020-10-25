"""added tsvector column and index for full text search

Revision ID: 81bc3c4ff4a4
Revises: e2d73cd9f007
Create Date: 2020-10-25 10:33:39.259946

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '81bc3c4ff4a4'
down_revision = 'e2d73cd9f007'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('tsv_searchable_text', postgresql.TSVECTOR(), nullable=True))
    op.create_index('tsv_idx', 'show', ['tsv_searchable_text'], unique=False, postgresql_using='gin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('tsv_idx', table_name='show')
    op.drop_column('show', 'tsv_searchable_text')
    # ### end Alembic commands ###
