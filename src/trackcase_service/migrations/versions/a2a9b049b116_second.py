"""second

Revision ID: a2a9b049b116
Revises: caa68e9cb33c
Create Date: 2023-11-25 10:39:57.618888

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a2a9b049b116"
down_revision: Union[str, None] = "caa68e9cb33c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "case_collection", sa.Column("status", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "case_collection", sa.Column("status_date", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "cash_collection", sa.Column("status", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "cash_collection", sa.Column("status_date", sa.DateTime(), nullable=True)
    )
    op.add_column("client", sa.Column("status", sa.String(length=100), nullable=True))
    op.add_column("client", sa.Column("status_date", sa.DateTime(), nullable=True))
    op.add_column("court", sa.Column("status", sa.String(length=100), nullable=True))
    op.add_column("court", sa.Column("status_date", sa.DateTime(), nullable=True))
    op.add_column(
        "court_case", sa.Column("status", sa.String(length=100), nullable=True)
    )
    op.add_column("court_case", sa.Column("status_date", sa.DateTime(), nullable=True))
    op.add_column("form", sa.Column("status", sa.String(length=100), nullable=True))
    op.add_column("form", sa.Column("status_date", sa.DateTime(), nullable=True))
    op.add_column(
        "hearing_calendar", sa.Column("status", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "hearing_calendar", sa.Column("status_date", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "history_case_collection",
        sa.Column("status", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "history_case_collection",
        sa.Column("status_date", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "history_cash_collection",
        sa.Column("status", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "history_cash_collection",
        sa.Column("status_date", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "history_client", sa.Column("status", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "history_client", sa.Column("status_date", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "history_court", sa.Column("status", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "history_court", sa.Column("status_date", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "history_court_case", sa.Column("status", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "history_court_case", sa.Column("status_date", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "history_form", sa.Column("status", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "history_form", sa.Column("status_date", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "history_hearing_calendar",
        sa.Column("status", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "history_hearing_calendar",
        sa.Column("status_date", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "history_judge", sa.Column("status", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "history_judge", sa.Column("status_date", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "history_task_calendar",
        sa.Column("status", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "history_task_calendar", sa.Column("status_date", sa.DateTime(), nullable=True)
    )
    op.add_column("judge", sa.Column("status", sa.String(length=100), nullable=True))
    op.add_column("judge", sa.Column("status_date", sa.DateTime(), nullable=True))
    op.add_column(
        "task_calendar", sa.Column("status", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "task_calendar", sa.Column("status_date", sa.DateTime(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("task_calendar", "status_date")
    op.drop_column("task_calendar", "status")
    op.drop_column("judge", "status_date")
    op.drop_column("judge", "status")
    op.drop_column("history_task_calendar", "status_date")
    op.drop_column("history_task_calendar", "status")
    op.drop_column("history_judge", "status_date")
    op.drop_column("history_judge", "status")
    op.drop_column("history_hearing_calendar", "status_date")
    op.drop_column("history_hearing_calendar", "status")
    op.drop_column("history_form", "status_date")
    op.drop_column("history_form", "status")
    op.drop_column("history_court_case", "status_date")
    op.drop_column("history_court_case", "status")
    op.drop_column("history_court", "status_date")
    op.drop_column("history_court", "status")
    op.drop_column("history_client", "status_date")
    op.drop_column("history_client", "status")
    op.drop_column("history_cash_collection", "status_date")
    op.drop_column("history_cash_collection", "status")
    op.drop_column("history_case_collection", "status_date")
    op.drop_column("history_case_collection", "status")
    op.drop_column("hearing_calendar", "status_date")
    op.drop_column("hearing_calendar", "status")
    op.drop_column("form", "status_date")
    op.drop_column("form", "status")
    op.drop_column("court_case", "status_date")
    op.drop_column("court_case", "status")
    op.drop_column("court", "status_date")
    op.drop_column("court", "status")
    op.drop_column("client", "status_date")
    op.drop_column("client", "status")
    op.drop_column("cash_collection", "status_date")
    op.drop_column("cash_collection", "status")
    op.drop_column("case_collection", "status_date")
    op.drop_column("case_collection", "status")
    # ### end Alembic commands ###