"""Actualizar modelo Post y agregar relaciones con categorías

Revision ID: bbb3c74f96f8
Revises: 04621a78b539
Create Date: 2024-12-12 18:22:31.753617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbb3c74f96f8'
down_revision = '04621a78b539'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('summary',
               existing_type=sa.VARCHAR(length=300),
               type_=sa.String(length=500),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('summary',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(length=300),
               existing_nullable=True)

    # ### end Alembic commands ###
