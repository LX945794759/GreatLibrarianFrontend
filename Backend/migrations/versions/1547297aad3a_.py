"""empty message

Revision ID: 1547297aad3a
Revises: 14aa1630cbb8
Create Date: 2024-04-25 11:07:40.514860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1547297aad3a'
down_revision = '14aa1630cbb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_TestProject', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tP_type', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_TestProject', schema=None) as batch_op:
        batch_op.drop_column('tP_type')

    # ### end Alembic commands ###
