"""empty message

Revision ID: 129e19157cb6
Revises: 
Create Date: 2017-03-28 11:23:22.515000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '129e19157cb6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body_html', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'body_html')
    # ### end Alembic commands ###