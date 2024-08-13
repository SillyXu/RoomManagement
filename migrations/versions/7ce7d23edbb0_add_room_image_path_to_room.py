"""Add room_image_path to Room

Revision ID: 7ce7d23edbb0
Revises: 6970a42e2d94
Create Date: 2024-08-09 17:04:26.997274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ce7d23edbb0'
down_revision = '6970a42e2d94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.add_column(sa.Column('room_image_path', sa.String(length=255), nullable=True))
        batch_op.drop_column('room_image')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.add_column(sa.Column('room_image', sa.BLOB(), nullable=True))
        batch_op.drop_column('room_image_path')

    # ### end Alembic commands ###