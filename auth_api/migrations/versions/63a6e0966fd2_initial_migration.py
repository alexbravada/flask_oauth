"""Initial migration

Revision ID: 63a6e0966fd2
Revises: 
Create Date: 2022-08-30 14:55:16.647252

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '63a6e0966fd2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    op.create_table('auth_history',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_device_type', sa.Enum('WEB', 'MOBILE', 'SMART', name='userdevicetype'), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_agent', sa.String(length=255), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_device_type'),
    sa.UniqueConstraint('id', 'user_device_type'),
    postgresql_partition_by='LIST (user_device_type)'
    )
    op.create_table('users_roles',
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('role_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###

    op.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_smart" PARTITION OF "auth_history" FOR VALUES IN ('SMART')"""
    )
    op.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_mobile" PARTITION OF "auth_history" FOR VALUES IN ('MOBILE')""")
    op.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_web" PARTITION OF "auth_history" FOR VALUES IN ('WEB')""")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_roles')
    op.drop_table('auth_history')
    op.drop_table('users')
    op.drop_table('roles')
    # ### end Alembic commands ###
