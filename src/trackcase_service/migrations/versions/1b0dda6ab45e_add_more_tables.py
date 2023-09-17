"""Add More Tables

Revision ID: 1b0dda6ab45e
Revises: 3a244a617255
Create Date: 2023-09-16 19:09:34.475512

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1b0dda6ab45e"
down_revision: Union[str, None] = "3a244a617255"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "collection",
        sa.Column("collection_date", sa.DateTime(), nullable=False),
        sa.Column("quote_amount", sa.BigInteger(), nullable=False),
        sa.Column("collected_amount", sa.BigInteger(), nullable=True),
        sa.Column("collection_method_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["collection_method_id"],
            ["collection_method.id"],
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "form",
        sa.Column("submit_date", sa.DateTime(), nullable=True),
        sa.Column("receipt_date", sa.DateTime(), nullable=True),
        sa.Column("rfe_date", sa.DateTime(), nullable=True),
        sa.Column("rfe_submit_date", sa.DateTime(), nullable=True),
        sa.Column("decision_date", sa.DateTime(), nullable=True),
        sa.Column("form_status_id", sa.Integer(), nullable=False),
        sa.Column("form_type_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["form_status_id"],
            ["form_status.id"],
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["form_type_id"], ["form_type.id"], onupdate="CASCADE", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "hearing_calendar",
        sa.Column("hearing_date", sa.DateTime(), nullable=False),
        sa.Column("hearing_type_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["hearing_type_id"],
            ["hearing_type.id"],
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "client",
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("a_number", sa.String(length=10), nullable=False),
        sa.Column("address", sa.String(length=100), nullable=False),
        sa.Column("phone", sa.String(length=10), nullable=False),
        sa.Column("email", sa.DateTime(), nullable=True),
        sa.Column("judge_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["judge_id"], ["judge.id"], onupdate="CASCADE", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("a_number"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("phone"),
    )
    op.create_table(
        "task_calendar",
        sa.Column("task_date", sa.DateTime(), nullable=False),
        sa.Column("task_type_id", sa.Integer(), nullable=False),
        sa.Column("hearing_calendar_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["hearing_calendar_id"],
            ["hearing_calendar.id"],
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["task_type_id"], ["task_type.id"], onupdate="CASCADE", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "court_case",
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["client_id"], ["client.id"], onupdate="CASCADE", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "task_calendar_form",
        sa.Column("form_id", sa.Integer(), nullable=False),
        sa.Column("task_calendar_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["form_id"], ["form.id"], onupdate="CASCADE", ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["task_calendar_id"],
            ["task_calendar.id"],
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "court_case_collection",
        sa.Column("case_id", sa.Integer(), nullable=False),
        sa.Column("collection_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["case_id"], ["court_case.id"], onupdate="CASCADE", ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["collection_id"],
            ["collection.id"],
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "court_case_form",
        sa.Column("case_id", sa.Integer(), nullable=False),
        sa.Column("form_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["case_id"], ["court_case.id"], onupdate="CASCADE", ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["form_id"], ["form.id"], onupdate="CASCADE", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "court_case_hearing_calendar",
        sa.Column("case_id", sa.Integer(), nullable=False),
        sa.Column("hearing_calendar_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["case_id"], ["court_case.id"], onupdate="CASCADE", ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["hearing_calendar_id"],
            ["hearing_calendar.id"],
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "court_case_task_calendar",
        sa.Column("case_id", sa.Integer(), nullable=False),
        sa.Column("task_calendar_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("sysdate"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["case_id"], ["court_case.id"], onupdate="CASCADE", ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["task_calendar_id"],
            ["task_calendar.id"],
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("court_case_task_calendar")
    op.drop_table("court_case_hearing_calendar")
    op.drop_table("court_case_form")
    op.drop_table("court_case_collection")
    op.drop_table("task_calendar_form")
    op.drop_table("court_case")
    op.drop_table("task_calendar")
    op.drop_table("client")
    op.drop_table("hearing_calendar")
    op.drop_table("form")
    op.drop_table("collection")
    # ### end Alembic commands ###