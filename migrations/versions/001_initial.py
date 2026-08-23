"""Initial schema.

Revision ID: 001
Revises:
Create Date: 2026-08-23 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('nationalities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_ar', sa.String(length=100), nullable=False),
    sa.Column('country_code', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('job_codes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=20), nullable=True),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('standard_rate', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('statuses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_ar', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('offices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('parent_office', sa.String(length=200), nullable=True),
    sa.Column('region', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('attendance_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('office_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['office_id'], ['offices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('employees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=400), nullable=False),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=True),
    sa.Column('id_number', sa.String(length=50), nullable=True),
    sa.Column('passport', sa.String(length=50), nullable=True),
    sa.Column('nationality_id', sa.Integer(), nullable=True),
    sa.Column('kafala', sa.String(length=200), nullable=True),
    sa.Column('job_code_id', sa.Integer(), nullable=True),
    sa.Column('unit_price', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('cbu', sa.String(length=5), nullable=True),
    sa.Column('region', sa.String(length=100), nullable=True),
    sa.Column('office_id', sa.Integer(), nullable=True),
    sa.Column('supervision_type', sa.String(length=50), nullable=True),
    sa.Column('attendance_group_id', sa.Integer(), nullable=True),
    sa.Column('direct_manager', sa.String(length=200), nullable=True),
    sa.Column('category', sa.String(length=100), nullable=True),
    sa.Column('profession', sa.String(length=200), nullable=True),
    sa.Column('qualification', sa.String(length=200), nullable=True),
    sa.Column('grad_year', sa.Integer(), nullable=True),
    sa.Column('experience_years', sa.Integer(), nullable=True),
    sa.Column('hire_date', sa.Date(), nullable=True),
    sa.Column('contract_end_date', sa.Date(), nullable=True),
    sa.Column('resignation_date', sa.Date(), nullable=True),
    sa.Column('current_status_id', sa.Integer(), nullable=True),
    sa.Column('status_reason', sa.Text(), nullable=True),
    sa.Column('is_replacement', sa.Boolean(), nullable=True),
    sa.Column('replaced_employee_id', sa.Integer(), nullable=True),
    sa.Column('replacement_start_date', sa.Date(), nullable=True),
    sa.Column('replacement_end_date', sa.Date(), nullable=True),
    sa.Column('serial_no', sa.String(length=50), nullable=True),
    sa.Column('re_code', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['attendance_group_id'], ['attendance_groups.id'], ),
    sa.ForeignKeyConstraint(['current_status_id'], ['statuses.id'], ),
    sa.ForeignKeyConstraint(['job_code_id'], ['job_codes.id'], ),
    sa.ForeignKeyConstraint(['nationality_id'], ['nationalities.id'], ),
    sa.ForeignKeyConstraint(['office_id'], ['offices.id'], ),
    sa.ForeignKeyConstraint(['replaced_employee_id'], ['employees.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employee_status_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employee_id', sa.Integer(), nullable=False),
    sa.Column('old_status', sa.String(length=100), nullable=True),
    sa.Column('new_status', sa.String(length=100), nullable=False),
    sa.Column('change_date', sa.Date(), nullable=False),
    sa.Column('reason', sa.Text(), nullable=True),
    sa.Column('recorded_by', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('employee_status_history')
    op.drop_table('employees')
    op.drop_table('users')
    op.drop_table('attendance_groups')
    op.drop_table('offices')
    op.drop_table('statuses')
    op.drop_table('job_codes')
    op.drop_table('nationalities')
