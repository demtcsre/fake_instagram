"""Initial migration.

Revision ID: b1c87c136fe5
Revises: d8526c7b9c4b
Create Date: 2023-11-18 23:29:26.027763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1c87c136fe5'
down_revision = 'd8526c7b9c4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('commented_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['commented_id'], ['id'])
        batch_op.drop_column('commented_by')

    with op.batch_alter_table('likes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])
        batch_op.drop_column('liked_by')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('likes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('liked_by', sa.INTEGER(), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['liked_by'], ['id'])
        batch_op.drop_column('user_id')

    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('commented_by', sa.INTEGER(), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['commented_by'], ['id'])
        batch_op.drop_column('commented_id')

    # ### end Alembic commands ###
