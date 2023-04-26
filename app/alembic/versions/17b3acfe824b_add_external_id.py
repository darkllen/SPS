"""add external id

Revision ID: 17b3acfe824b
Revises: f4eaa078c653
Create Date: 2023-04-26 22:31:33.698939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17b3acfe824b'
down_revision = 'f4eaa078c653'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('sensor_external_id', sa.String(length=255), nullable=False))
    op.add_column('sensors', sa.Column('external_id', sa.String(length=255), nullable=False))
    op.create_unique_constraint(None, 'sensors', ['external_id'])
    op.drop_constraint('events_sensor_id_fkey', 'events', type_='foreignkey')
    op.create_foreign_key(None, 'events', 'sensors', ['sensor_external_id'], ['external_id'])
    op.drop_column('events', 'sensor_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'sensors', type_='unique')
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.add_column('events', sa.Column('sensor_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('sensors', 'external_id')
    op.create_foreign_key('events_sensor_id_fkey', 'events', 'sensors', ['sensor_id'], ['id'])
    op.drop_column('events', 'sensor_external_id')
    # ### end Alembic commands ###