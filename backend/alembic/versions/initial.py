"""initial

Revision ID: initial
Revises:
Create Date: 2026-01-01
"""
from alembic import op
import sqlalchemy as sa

revision = 'initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('centers', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('name', sa.String(255), nullable=False), sa.Column('timezone', sa.String(64), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))
    op.create_table('users', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('center_id', sa.Integer(), sa.ForeignKey('centers.id'), nullable=False), sa.Column('email', sa.String(255), unique=True, nullable=False), sa.Column('password_hash', sa.String(512), nullable=False), sa.Column('full_name', sa.String(255), nullable=False), sa.Column('role', sa.Enum('student','teacher','manager','admin', name='userrole'), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))
    op.create_index('ix_users_center_role','users',['center_id','role'])
    op.create_index('ix_users_center_id','users',['center_id'])
    op.create_table('groups', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('center_id', sa.Integer(), sa.ForeignKey('centers.id'), nullable=False), sa.Column('owner_teacher_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False), sa.Column('name', sa.String(255), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))
    op.create_index('ix_groups_center_teacher','groups',['center_id','owner_teacher_id'])
    op.create_index('ix_groups_center_id','groups',['center_id'])
    op.create_table('enrollments', sa.Column('student_id', sa.Integer(), sa.ForeignKey('users.id'), primary_key=True), sa.Column('group_id', sa.Integer(), sa.ForeignKey('groups.id'), primary_key=True), sa.Column('center_id', sa.Integer(), sa.ForeignKey('centers.id'), nullable=False), sa.Column('status', sa.Enum('pending','approved','rejected', name='enrollmentstatus'), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))
    op.create_index('ix_enrollments_center_status','enrollments',['center_id','status'])
    op.create_index('ix_enrollments_center_id','enrollments',['center_id'])
    op.create_table('teacher_policies', sa.Column('teacher_id', sa.Integer(), sa.ForeignKey('users.id'), primary_key=True), sa.Column('center_id', sa.Integer(), sa.ForeignKey('centers.id'), nullable=False), sa.Column('max_points_per_award', sa.Integer(), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))
    op.create_index('ix_teacher_policies_center_id','teacher_policies',['center_id'])
    op.create_table('wallets', sa.Column('student_id', sa.Integer(), sa.ForeignKey('users.id'), primary_key=True), sa.Column('center_id', sa.Integer(), sa.ForeignKey('centers.id'), nullable=False), sa.Column('available_balance', sa.Integer(), nullable=False), sa.Column('held_balance', sa.Integer(), nullable=False), sa.Column('total_earned', sa.Integer(), nullable=False), sa.Column('total_spent', sa.Integer(), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))
    op.create_index('ix_wallets_center_id','wallets',['center_id'])
    op.create_table('products', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('center_id', sa.Integer(), sa.ForeignKey('centers.id'), nullable=False), sa.Column('name', sa.String(255), nullable=False), sa.Column('price', sa.Integer(), nullable=False), sa.Column('stock', sa.Integer(), nullable=False), sa.Column('is_active', sa.Boolean(), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))
    op.create_index('ix_products_center_active','products',['center_id','is_active'])
    op.create_index('ix_products_center_id','products',['center_id'])
    op.create_table('orders', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('center_id', sa.Integer(), sa.ForeignKey('centers.id'), nullable=False), sa.Column('student_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False), sa.Column('status', sa.Enum('created','approved','handed_over','completed','cancelled','rejected', name='orderstatus'), nullable=False), sa.Column('total_amount', sa.Integer(), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))
    op.create_index('ix_orders_center_status','orders',['center_id','status'])
    op.create_index('ix_orders_center_id','orders',['center_id'])
    op.create_table('order_items', sa.Column('order_id', sa.Integer(), sa.ForeignKey('orders.id'), primary_key=True), sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id'), primary_key=True), sa.Column('quantity', sa.Integer(), nullable=False), sa.Column('price_snapshot', sa.Integer(), nullable=False), sa.Column('product_name_snapshot', sa.String(255), nullable=False))
    op.create_table('transactions', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('center_id', sa.Integer(), sa.ForeignKey('centers.id'), nullable=False), sa.Column('student_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False), sa.Column('group_id', sa.Integer(), sa.ForeignKey('groups.id')), sa.Column('order_id', sa.Integer(), sa.ForeignKey('orders.id')), sa.Column('type', sa.Enum('award','hold','release','purchase', name='transactiontype'), nullable=False), sa.Column('amount', sa.Integer(), nullable=False), sa.Column('reason', sa.String(255), nullable=False), sa.Column('awarded_by', sa.Integer(), sa.ForeignKey('users.id')), sa.Column('award_date', sa.Date()), sa.Column('awarded_at', sa.DateTime(timezone=True)), sa.Column('available_after', sa.Integer(), nullable=False), sa.Column('held_after', sa.Integer(), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))
    op.create_index('ix_transactions_center_student','transactions',['center_id','student_id'])
    op.create_index('ix_transactions_center_id','transactions',['center_id'])
    op.execute("CREATE UNIQUE INDEX uq_award_once_per_day ON transactions (awarded_by, student_id, award_date) WHERE type = 'award'")
    op.create_table('reviews', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('center_id', sa.Integer(), sa.ForeignKey('centers.id'), nullable=False), sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id'), nullable=False), sa.Column('order_id', sa.Integer(), sa.ForeignKey('orders.id'), nullable=False), sa.Column('student_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False), sa.Column('rating', sa.Integer(), nullable=False), sa.Column('comment', sa.String(1000), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))
    op.create_index('ix_reviews_center_product','reviews',['center_id','product_id'])
    op.create_index('ix_reviews_center_id','reviews',['center_id'])
    op.create_table('audit_logs', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('center_id', sa.Integer(), sa.ForeignKey('centers.id'), nullable=False), sa.Column('actor_user_id', sa.Integer(), sa.ForeignKey('users.id')), sa.Column('action', sa.String(100), nullable=False), sa.Column('entity_type', sa.String(100), nullable=False), sa.Column('entity_id', sa.String(100), nullable=False), sa.Column('payload', sa.JSON(), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))
    op.create_index('ix_audit_logs_center_action','audit_logs',['center_id','action'])
    op.create_index('ix_audit_logs_center_id','audit_logs',['center_id'])
    op.create_table('idempotency_keys', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('key', sa.String(255), nullable=False), sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False), sa.Column('endpoint', sa.String(255), nullable=False), sa.Column('method', sa.String(16), nullable=False), sa.Column('status_code', sa.Integer(), nullable=False), sa.Column('response_body', sa.JSON(), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')), sa.UniqueConstraint('key','user_id','endpoint','method',name='uq_idempotency_key_scope'))
    op.create_table('refresh_tokens', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False), sa.Column('jti', sa.String(255), nullable=False, unique=True), sa.Column('token_hash', sa.String(128), nullable=False, unique=True), sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False), sa.Column('revoked_at', sa.DateTime(timezone=True)), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))
    op.create_index('ix_refresh_tokens_user_revoked','refresh_tokens',['user_id','revoked_at'])


def downgrade() -> None:
    op.drop_table('refresh_tokens'); op.drop_table('idempotency_keys'); op.drop_table('audit_logs'); op.drop_table('reviews'); op.drop_table('transactions'); op.drop_table('order_items'); op.drop_table('orders'); op.drop_table('products'); op.drop_table('wallets'); op.drop_table('teacher_policies'); op.drop_table('enrollments'); op.drop_table('groups'); op.drop_table('users'); op.drop_table('centers')
