"""empty message

Revision ID: 73a1ed272fc8
Revises: ae67a914460f
Create Date: 2024-03-31 16:27:08.526509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73a1ed272fc8'
down_revision = 'ae67a914460f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], ),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('favorite_planet')
    op.drop_table('favorite_character')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite_character',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('character_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], name='favorite_character_character_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='favorite_character_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='favorite_character_pkey')
    )
    op.create_table('favorite_planet',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], name='favorite_planet_planet_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='favorite_planet_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='favorite_planet_pkey')
    )
    op.drop_table('favorite')
    # ### end Alembic commands ###