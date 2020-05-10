"""empty message

Revision ID: bad663e7e10e
Revises: 
Create Date: 2020-05-09 16:47:17.699382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bad663e7e10e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actors',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('release_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movies_actors',
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('actor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
    sa.PrimaryKeyConstraint('movie_id', 'actor_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movies_actors')
    op.drop_table('movies')
    op.drop_table('actors')
    # ### end Alembic commands ###