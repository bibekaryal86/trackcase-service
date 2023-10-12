"""First

Revision ID: 16b712957483
Revises:
Create Date: 2023-10-11 21:10:11.306103

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "16b712957483"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "case_type",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=3000), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "collection_method",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=3000), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "court",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("address", sa.String(length=1000), nullable=False),
        sa.Column("dhs_address", sa.String(length=1000), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("address"),
        sa.UniqueConstraint("dhs_address"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "form_status",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=3000), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "form_type",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=3000), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "hearing_type",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=3000), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "task_type",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=3000), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "zest_table",
        sa.Column("test", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("test"),
    )
    op.create_table(
        "judge",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("webex", sa.String(length=1000), nullable=True),
        sa.Column("court_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["court_id"], ["court.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("webex"),
    )
    op.create_table(
        "client",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("a_number", sa.String(length=100), nullable=True),
        sa.Column("address", sa.String(length=1000), nullable=False),
        sa.Column("phone", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("judge_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["judge_id"], ["judge.id"], onupdate="NO ACTION", ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("a_number"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("phone"),
    )
    op.create_table(
        "court_case",
        sa.Column("case_type_id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
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
        "hearing_calendar",
        sa.Column("hearing_date", sa.DateTime(), nullable=False),
        sa.Column("hearing_type_id", sa.Integer(), nullable=False),
        sa.Column("court_case_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
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
        "task_calendar",
        sa.Column("task_date", sa.DateTime(), nullable=False),
        sa.Column("task_type_id", sa.Integer(), nullable=False),
        sa.Column("court_case_id", sa.Integer(), nullable=False),
        sa.Column("hearing_calendar_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
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
        sa.Column("rfe_date", sa.DateTime(), nullable=True),
        sa.Column("rfe_submit_date", sa.DateTime(), nullable=True),
        sa.Column("decision_date", sa.DateTime(), nullable=True),
        sa.Column("form_type_id", sa.Integer(), nullable=False),
        sa.Column("form_status_id", sa.Integer(), nullable=False),
        sa.Column("court_case_id", sa.Integer(), nullable=False),
        sa.Column("task_calendar_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["court_case_id"],
            ["court_case.id"],
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["form_status_id"],
            ["form_status.id"],
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
        "case_collection",
        sa.Column("quote_date", sa.DateTime(), nullable=False),
        sa.Column("quote_amount", sa.BigInteger(), nullable=False),
        sa.Column("initial_payment", sa.BigInteger(), nullable=False),
        sa.Column("collection_method_id", sa.Integer(), nullable=False),
        sa.Column("court_case_id", sa.Integer(), nullable=False),
        sa.Column("form_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("now()"), nullable=False
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
        "history_form",
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("submit_date", sa.DateTime(), nullable=True),
        sa.Column("receipt_date", sa.DateTime(), nullable=True),
        sa.Column("rfe_date", sa.DateTime(), nullable=True),
        sa.Column("rfe_submit_date", sa.DateTime(), nullable=True),
        sa.Column("decision_date", sa.DateTime(), nullable=True),
        sa.Column("form_id", sa.Integer(), nullable=False),
        sa.Column("form_type_id", sa.Integer(), nullable=False),
        sa.Column("form_status_id", sa.Integer(), nullable=False),
        sa.Column("court_case_id", sa.Integer(), nullable=False),
        sa.Column("task_calendar_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("now()"), nullable=False
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
        sa.ForeignKeyConstraint(
            ["form_status_id"],
            ["form_status.id"],
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
        "cash_collection",
        sa.Column("collection_date", sa.DateTime(), nullable=False),
        sa.Column("collected_amount", sa.BigInteger(), nullable=False),
        sa.Column("waived_amount", sa.BigInteger(), nullable=False),
        sa.Column("memo", sa.String(length=3000), nullable=True),
        sa.Column("case_collection_id", sa.Integer(), nullable=False),
        sa.Column("collection_method_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
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
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("cash_collection")
    op.drop_table("history_form")
    op.drop_table("case_collection")
    op.drop_table("form")
    op.drop_table("task_calendar")
    op.drop_table("hearing_calendar")
    op.drop_table("court_case")
    op.drop_table("client")
    op.drop_table("judge")
    op.drop_table("zest_table")
    op.drop_table("task_type")
    op.drop_table("hearing_type")
    op.drop_table("form_type")
    op.drop_table("form_status")
    op.drop_table("court")
    op.drop_table("collection_method")
    op.drop_table("case_type")
    # ### end Alembic commands ###
