"""empty message

Revision ID: 921a5d3fcdc4
Revises: e3038eabfc12
Create Date: 2024-04-23 20:05:47.018132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '921a5d3fcdc4'
down_revision = 'e3038eabfc12'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status_id', sa.String(), nullable=True))
        batch_op.create_foreign_key('fk_item_status_id', 'status', ['status_id'], ['id'])
        batch_op.drop_column('item_status')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('item_status', sa.BOOLEAN(), nullable=True))
        batch_op.drop_constraint('fk_item_status_id', type_='foreignkey')
        batch_op.drop_column('status_id')

    # ### end Alembic commands ###
