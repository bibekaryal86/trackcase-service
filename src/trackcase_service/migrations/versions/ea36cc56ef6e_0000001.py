"""0000001

Revision ID: ea36cc56ef6e
Revises:
Create Date: 2023-12-24 15:42:13.706342

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "23b617e5adef"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "case_type",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=3000), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "collection_method",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=3000), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "court",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("dhs_address", sa.String(length=1000), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("street_address", sa.String(length=500), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=10), nullable=True),
        sa.Column("zip_code", sa.String(length=10), nullable=True),
        sa.Column("phone_number", sa.String(length=25), nullable=True),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "form_type",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=3000), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "hearing_type",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=3000), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "task_type",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=3000), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "history_court",
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("court_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.Column("dhs_address", sa.String(length=1000), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("street_address", sa.String(length=500), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=10), nullable=True),
        sa.Column("zip_code", sa.String(length=10), nullable=True),
        sa.Column("phone_number", sa.String(length=25), nullable=True),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["court_id"], ["court.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "judge",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("webex", sa.String(length=1000), nullable=True),
        sa.Column("court_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["court_id"], ["court.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("webex"),
    )
    op.create_table(
        "note_court",
        sa.Column("court_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("note", sa.String(length=3000), nullable=False),
        sa.ForeignKeyConstraint(
            ["court_id"], ["court.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "client",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("a_number", sa.String(length=100), nullable=True),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("judge_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("street_address", sa.String(length=500), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=10), nullable=True),
        sa.Column("zip_code", sa.String(length=10), nullable=True),
        sa.Column("phone_number", sa.String(length=25), nullable=True),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["judge_id"], ["judge.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("a_number"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "history_judge",
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("judge_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.Column("webex", sa.String(length=1000), nullable=True),
        sa.Column("court_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["court_id"], ["court.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["judge_id"], ["judge.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "note_judge",
        sa.Column("judge_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("note", sa.String(length=3000), nullable=False),
        sa.ForeignKeyConstraint(
            ["judge_id"], ["judge.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "court_case",
        sa.Column("case_type_id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["case_type_id"],
            ["case_type.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["client_id"], ["client.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "history_client",
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.Column("a_number", sa.String(length=100), nullable=True),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("judge_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("street_address", sa.String(length=500), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=10), nullable=True),
        sa.Column("zip_code", sa.String(length=10), nullable=True),
        sa.Column("phone_number", sa.String(length=25), nullable=True),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["client_id"], ["client.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["judge_id"], ["judge.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "note_client",
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("note", sa.String(length=3000), nullable=False),
        sa.ForeignKeyConstraint(
            ["client_id"], ["client.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "hearing_calendar",
        sa.Column("hearing_date", sa.DateTime(), nullable=False),
        sa.Column("hearing_type_id", sa.Integer(), nullable=False),
        sa.Column("court_case_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["court_case_id"],
            ["court_case.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["hearing_type_id"],
            ["hearing_type.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "history_court_case",
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("court_case_id", sa.Integer(), nullable=False),
        sa.Column("case_type_id", sa.Integer(), nullable=True),
        sa.Column("client_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["case_type_id"],
            ["case_type.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["client_id"], ["client.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["court_case_id"],
            ["court_case.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "note_court_case",
        sa.Column("court_case_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("note", sa.String(length=3000), nullable=False),
        sa.ForeignKeyConstraint(
            ["court_case_id"],
            ["court_case.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "history_hearing_calendar",
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("hearing_calendar_id", sa.Integer(), nullable=False),
        sa.Column("hearing_date", sa.DateTime(), nullable=True),
        sa.Column("hearing_type_id", sa.Integer(), nullable=True),
        sa.Column("court_case_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["court_case_id"],
            ["court_case.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["hearing_calendar_id"],
            ["hearing_calendar.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["hearing_type_id"],
            ["hearing_type.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "note_hearing_calendar",
        sa.Column("hearing_calendar_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("note", sa.String(length=3000), nullable=False),
        sa.ForeignKeyConstraint(
            ["hearing_calendar_id"],
            ["hearing_calendar.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "task_calendar",
        sa.Column("task_date", sa.DateTime(), nullable=False),
        sa.Column("task_type_id", sa.Integer(), nullable=False),
        sa.Column("court_case_id", sa.Integer(), nullable=False),
        sa.Column("hearing_calendar_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["court_case_id"],
            ["court_case.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["hearing_calendar_id"],
            ["hearing_calendar.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["task_type_id"],
            ["task_type.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "form",
        sa.Column("submit_date", sa.DateTime(), nullable=True),
        sa.Column("receipt_date", sa.DateTime(), nullable=True),
        sa.Column("receipt_number", sa.String(length=100), nullable=True),
        sa.Column("priority_date", sa.DateTime(), nullable=True),
        sa.Column("rfe_date", sa.DateTime(), nullable=True),
        sa.Column("rfe_submit_date", sa.DateTime(), nullable=True),
        sa.Column("decision_date", sa.DateTime(), nullable=True),
        sa.Column("form_type_id", sa.Integer(), nullable=False),
        sa.Column("court_case_id", sa.Integer(), nullable=False),
        sa.Column("task_calendar_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["court_case_id"],
            ["court_case.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["form_type_id"],
            ["form_type.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["task_calendar_id"],
            ["task_calendar.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "history_task_calendar",
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("task_calendar_id", sa.Integer(), nullable=False),
        sa.Column("task_date", sa.DateTime(), nullable=True),
        sa.Column("task_type_id", sa.Integer(), nullable=True),
        sa.Column("court_case_id", sa.Integer(), nullable=True),
        sa.Column("hearing_calendar_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["court_case_id"],
            ["court_case.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["hearing_calendar_id"],
            ["hearing_calendar.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["task_calendar_id"],
            ["task_calendar.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["task_type_id"],
            ["task_type.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "note_task_calendar",
        sa.Column("task_calendar_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("note", sa.String(length=3000), nullable=False),
        sa.ForeignKeyConstraint(
            ["task_calendar_id"],
            ["task_calendar.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "case_collection",
        sa.Column("quote_date", sa.DateTime(), nullable=False),
        sa.Column("quote_amount", sa.BigInteger(), nullable=False),
        sa.Column("initial_payment", sa.BigInteger(), nullable=False),
        sa.Column("collection_method_id", sa.Integer(), nullable=False),
        sa.Column("court_case_id", sa.Integer(), nullable=False),
        sa.Column("form_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["collection_method_id"],
            ["collection_method.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["court_case_id"],
            ["court_case.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["form_id"], ["form.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "history_form",
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("form_id", sa.Integer(), nullable=False),
        sa.Column("submit_date", sa.DateTime(), nullable=True),
        sa.Column("receipt_date", sa.DateTime(), nullable=True),
        sa.Column("receipt_number", sa.String(length=100), nullable=True),
        sa.Column("priority_date", sa.DateTime(), nullable=True),
        sa.Column("rfe_date", sa.DateTime(), nullable=True),
        sa.Column("rfe_submit_date", sa.DateTime(), nullable=True),
        sa.Column("decision_date", sa.DateTime(), nullable=True),
        sa.Column("form_type_id", sa.Integer(), nullable=True),
        sa.Column("court_case_id", sa.Integer(), nullable=True),
        sa.Column("task_calendar_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["court_case_id"],
            ["court_case.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["form_id"], ["form.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["form_type_id"],
            ["form_type.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["task_calendar_id"],
            ["task_calendar.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "note_form",
        sa.Column("form_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("note", sa.String(length=3000), nullable=False),
        sa.ForeignKeyConstraint(
            ["form_id"], ["form.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "cash_collection",
        sa.Column("collection_date", sa.DateTime(), nullable=False),
        sa.Column("collected_amount", sa.BigInteger(), nullable=False),
        sa.Column("waived_amount", sa.BigInteger(), nullable=False),
        sa.Column("memo", sa.String(length=3000), nullable=True),
        sa.Column("case_collection_id", sa.Integer(), nullable=False),
        sa.Column("collection_method_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["case_collection_id"],
            ["case_collection.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["collection_method_id"],
            ["collection_method.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "history_case_collection",
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("case_collection_id", sa.Integer(), nullable=False),
        sa.Column("quote_date", sa.DateTime(), nullable=True),
        sa.Column("quote_amount", sa.BigInteger(), nullable=True),
        sa.Column("initial_payment", sa.BigInteger(), nullable=True),
        sa.Column("collection_method_id", sa.Integer(), nullable=True),
        sa.Column("court_case_id", sa.Integer(), nullable=True),
        sa.Column("form_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["case_collection_id"],
            ["case_collection.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["collection_method_id"],
            ["collection_method.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["court_case_id"],
            ["court_case.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["form_id"], ["form.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "note_case_collection",
        sa.Column("case_collection_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("note", sa.String(length=3000), nullable=False),
        sa.ForeignKeyConstraint(
            ["case_collection_id"],
            ["case_collection.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "history_cash_collection",
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("cash_collection_id", sa.Integer(), nullable=False),
        sa.Column("collection_date", sa.DateTime(), nullable=True),
        sa.Column("collected_amount", sa.BigInteger(), nullable=True),
        sa.Column("waived_amount", sa.BigInteger(), nullable=True),
        sa.Column("memo", sa.String(length=3000), nullable=True),
        sa.Column("case_collection_id", sa.Integer(), nullable=True),
        sa.Column("collection_method_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["case_collection_id"],
            ["case_collection.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["cash_collection_id"],
            ["cash_collection.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["collection_method_id"],
            ["collection_method.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "note_cash_collection",
        sa.Column("cash_collection_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("note", sa.String(length=3000), nullable=False),
        sa.ForeignKeyConstraint(
            ["cash_collection_id"],
            ["cash_collection.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "zest_table",
        sa.Column("test", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("test"),
    )
    op.execute("INSERT INTO zest_table (test) VALUES ('database')")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("note_cash_collection")
    op.drop_table("history_cash_collection")
    op.drop_table("note_case_collection")
    op.drop_table("history_case_collection")
    op.drop_table("cash_collection")
    op.drop_table("note_form")
    op.drop_table("history_form")
    op.drop_table("case_collection")
    op.drop_table("note_task_calendar")
    op.drop_table("history_task_calendar")
    op.drop_table("form")
    op.drop_table("task_calendar")
    op.drop_table("note_hearing_calendar")
    op.drop_table("history_hearing_calendar")
    op.drop_table("note_court_case")
    op.drop_table("history_court_case")
    op.drop_table("hearing_calendar")
    op.drop_table("note_client")
    op.drop_table("history_client")
    op.drop_table("court_case")
    op.drop_table("note_judge")
    op.drop_table("history_judge")
    op.drop_table("client")
    op.drop_table("note_court")
    op.drop_table("judge")
    op.drop_table("history_court")
    op.drop_table("zest_table")
    op.drop_table("task_type")
    op.drop_table("hearing_type")
    op.drop_table("form_type")
    op.drop_table("court")
    op.drop_table("collection_method")
    op.drop_table("case_type")
    # ### end Alembic commands ###
