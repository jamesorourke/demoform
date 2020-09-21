"""census table

Revision ID: d82aca8a69d7
Revises: 065a5bdd4775
Create Date: 2020-09-16 11:24:38.795282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd82aca8a69d7'
down_revision = '065a5bdd4775'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('census',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('dob', sa.Date(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_census_dob'), 'census', ['dob'], unique=False)
    op.create_index(op.f('ix_census_name'), 'census', ['name'], unique=False)
    op.create_index(op.f('ix_census_timestamp'), 'census', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_census_timestamp'), table_name='census')
    op.drop_index(op.f('ix_census_name'), table_name='census')
    op.drop_index(op.f('ix_census_dob'), table_name='census')
    op.drop_table('census')
    # ### end Alembic commands ###