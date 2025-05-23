"""add tenant id support for eval

Revision ID: ea2679878e00
Revises: a9c87d84b974
Create Date: 2025-04-14 15:53:25.261204

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import core.db_models.utils


# revision identifiers, used by Alembic.
revision: str = 'ea2679878e00'
down_revision: Union[str, None] = 'a9c87d84b974'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


tables = ['eval_config', 'eval_config_history', 'eval_result_prompt', 'eval_result_response', 'eval_run', 'eval_target']


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Adding tenant_id column to guardrail tables by executing queries instead of using op.add_column
    # because it doesn't add columns with default values and NOT NULL together
    with op.batch_alter_table('eval_target', recreate='always') as batch_op:
        batch_op.alter_column(
            'application_id',
            existing_type=sa.Integer(),
            nullable=True,
        )

    connection = op.get_bind()
    for table in tables:
        connection.execute(
            sa.text(f"ALTER TABLE {table} ADD COLUMN tenant_id VARCHAR(255) NOT NULL DEFAULT 1")
        )
        op.create_index(f'ix_{table}_tenant_id', table, ['tenant_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'eval_target', 'ai_application', ['application_id'], ['id'])
    for table in tables:
        op.drop_index(f'ix_{table}_tenant_id', table_name=table)
        op.drop_column(table, 'tenant_id')
    # ### end Alembic commands ###