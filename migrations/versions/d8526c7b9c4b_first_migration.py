"""First migration

Revision ID: d8526c7b9c4b
Revises: 
Create Date: 2023-10-26 16:28:59.155985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8526c7b9c4b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('fullname', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('profile_pic', sa.String(length=128), nullable=True),
    sa.Column('bio', sa.String(length=128), nullable=True),
    sa.Column('join_date', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('photo', sa.String(length=256), nullable=False),
    sa.Column('caption', sa.String(length=256), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('post_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('relations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('following_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=256), nullable=False),
    sa.Column('relation_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['following_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('commented_by', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(length=256), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('comment_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['commented_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('liked_by', sa.Integer(), nullable=False),
    sa.Column('like_count', sa.Integer(), nullable=False),
    sa.Column('like_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['liked_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    op.drop_table('comments')
    op.drop_table('relations')
    op.drop_table('posts')
    op.drop_table('users')
    # ### end Alembic commands ###