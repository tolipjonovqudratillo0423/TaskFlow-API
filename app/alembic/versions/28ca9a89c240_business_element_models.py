"""Business element models

Revision ID: 28ca9a89c240
Revises: c7de71c6d7a6
Create Date: 2026-07-20 18:50:26.061277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28ca9a89c240'
down_revision: Union[str, Sequence[str], None] = 'c7de71c6d7a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    project_status = sa.Enum('active', 'archived', name='projectstatus')
    task_status = sa.Enum('todo', 'in_progress', 'done', name='taskstatus')
    project_status.create(op.get_bind())
    task_status.create(op.get_bind())

    op.create_index(op.f('ix_comments_author_id'), 'comments', ['author_id'], unique=False)
    op.create_index(op.f('ix_comments_task_id'), 'comments', ['task_id'], unique=False)
    op.alter_column('projects', 'status',
               existing_type=sa.VARCHAR(),
               type_=project_status,
               postgresql_using='status::projectstatus',
               existing_nullable=False)
    op.create_index(op.f('ix_projects_owner_id'), 'projects', ['owner_id'], unique=False)
    op.create_index(op.f('ix_projects_status'), 'projects', ['status'], unique=False)
    op.alter_column('tasks', 'status',
               existing_type=sa.VARCHAR(),
               type_=task_status,
               postgresql_using='status::taskstatus',
               existing_nullable=False)
    op.create_index(op.f('ix_tasks_assignee_id'), 'tasks', ['assignee_id'], unique=False)
    op.create_index(op.f('ix_tasks_project_id'), 'tasks', ['project_id'], unique=False)
    op.create_index(op.f('ix_tasks_status'), 'tasks', ['status'], unique=False)
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_unique_constraint(None, 'users', ['phone_number'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.drop_index(op.f('ix_tasks_status'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_project_id'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_assignee_id'), table_name='tasks')
    op.alter_column('tasks', 'status',
               existing_type=sa.Enum('todo', 'in_progress', 'done', name='taskstatus'),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    op.drop_index(op.f('ix_projects_status'), table_name='projects')
    op.drop_index(op.f('ix_projects_owner_id'), table_name='projects')
    op.alter_column('projects', 'status',
               existing_type=sa.Enum('active', 'archived', name='projectstatus'),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    op.drop_index(op.f('ix_comments_task_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_author_id'), table_name='comments')

    sa.Enum(name='taskstatus').drop(op.get_bind())
    sa.Enum(name='projectstatus').drop(op.get_bind())