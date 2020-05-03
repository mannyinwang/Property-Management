"""empty message

Revision ID: 05fa250eee9b
Revises: 
Create Date: 2020-04-19 03:46:40.461796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05fa250eee9b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=45), nullable=True),
    sa.Column('last_name', sa.String(length=45), nullable=True),
    sa.Column('email', sa.String(length=45), nullable=True),
    sa.Column('password', sa.String(length=45), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('apt_categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=45), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=45), nullable=True),
    sa.Column('last_name', sa.String(length=45), nullable=True),
    sa.Column('email', sa.String(length=45), nullable=True),
    sa.Column('password', sa.String(length=45), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('position', sa.String(length=45), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('apartments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('apartment_number', sa.String(length=20), nullable=True),
    sa.Column('number_of_room', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['apt_categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tenants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=45), nullable=True),
    sa.Column('last_name', sa.String(length=45), nullable=True),
    sa.Column('phone', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=45), nullable=True),
    sa.Column('password', sa.String(length=150), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('apartment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['apartment_id'], ['apartments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tenants')
    op.drop_table('apartments')
    op.drop_table('employees')
    op.drop_table('apt_categories')
    op.drop_table('admins')
    # ### end Alembic commands ###
