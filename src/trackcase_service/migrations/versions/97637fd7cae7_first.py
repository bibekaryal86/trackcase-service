"""first

Revision ID: 97637fd7cae7
Revises:
Create Date: 2024-02-05 23:42:50.572015

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "97637fd7cae7"
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
            ["court_id"],
            ["court.id"],
            name="history_court_court_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
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
            ["court_id"],
            ["court.id"],
            name="judge_court_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("webex"),
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
            ["judge_id"],
            ["judge.id"],
            name="client_judge_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
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
            ["court_id"],
            ["court.id"],
            name="history_judge_court_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["judge_id"],
            ["judge.id"],
            name="history_judge_judge_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
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
            name="court_case_case_type_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["client.id"],
            name="court_case_client_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
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
            ["client_id"],
            ["client.id"],
            name="history_client_client_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["judge_id"],
            ["judge.id"],
            name="history_client_judge_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "case_collection",
        sa.Column("quote_date", sa.DateTime(), nullable=False),
        sa.Column("quote_amount", sa.BigInteger(), nullable=False),
        sa.Column("court_case_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["court_case_id"],
            ["court_case.id"],
            name="case_collection_court_case_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("court_case_id"),
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
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["court_case_id"],
            ["court_case.id"],
            name="form_court_case_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["form_type_id"],
            ["form_type.id"],
            name="form_form_type_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
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
            name="hearing_calendar_court_case_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["hearing_type_id"],
            ["hearing_type.id"],
            name="hearing_calendar_hearing_type_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("court_case_id"),
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
            name="history_court_case_case_type_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["client.id"],
            name="history_court_case_client_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["court_case_id"],
            ["court_case.id"],
            name="history_court_case_court_case_id",
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
        sa.Column("memo", sa.String(length=3000), nullable=False),
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
            name="cash_collection_case_collection_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["collection_method_id"],
            ["collection_method.id"],
            name="cash_collection_collection_method_id",
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
        sa.Column("court_case_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["case_collection_id"],
            ["case_collection.id"],
            name="history_case_collection_case_collection_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["court_case_id"],
            ["court_case.id"],
            name="history_case_collection_court_case_id",
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
            name="history_hearing_calendar_court_case_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["hearing_calendar_id"],
            ["hearing_calendar.id"],
            name="history_hearing_calendar_hearing_calendar_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["hearing_type_id"],
            ["hearing_type.id"],
            name="history_hearing_calendar_hearing_type_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "task_calendar",
        sa.Column("task_date", sa.DateTime(), nullable=False),
        sa.Column("due_date", sa.DateTime(), nullable=False),
        sa.Column("task_type_id", sa.Integer(), nullable=False),
        sa.Column("hearing_calendar_id", sa.Integer(), nullable=True),
        sa.Column("form_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["form_id"],
            ["form.id"],
            name="task_calendar_form_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["hearing_calendar_id"],
            ["hearing_calendar.id"],
            name="task_calendar_hearing_calendar_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["task_type_id"],
            ["task_type.id"],
            name="task_calendar_task_type_id",
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
            name="history_cash_collection_case_collection_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["cash_collection_id"],
            ["cash_collection.id"],
            name="history_cash_collection_cash_collection_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["collection_method_id"],
            ["collection_method.id"],
            name="history_cash_collection_collection_method_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
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
            name="history_form_court_case_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["form_id"],
            ["form.id"],
            name="history_form_form_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["form_type_id"],
            ["form_type.id"],
            name="history_form_form_type_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["task_calendar_id"],
            ["task_calendar.id"],
            name="history_form_task_calendar_id",
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
        sa.Column("due_date", sa.DateTime(), nullable=True),
        sa.Column("task_type_id", sa.Integer(), nullable=True),
        sa.Column("hearing_calendar_id", sa.Integer(), nullable=True),
        sa.Column("form_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.ForeignKeyConstraint(
            ["form_id"],
            ["form.id"],
            name="history_task_calendar_form_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["hearing_calendar_id"],
            ["hearing_calendar.id"],
            name="history_task_calendar_hearing_calendar_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["task_calendar_id"],
            ["task_calendar.id"],
            name="history_task_calendar_task_calendar_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["task_type_id"],
            ["task_type.id"],
            name="history_task_calendar_task_type_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # other migrations
    op.execute(
        """INSERT INTO task_type (created, modified, name, description) VALUES (now(), now(), 'Due at Hearing', 'Due at Hearing')"""  # noqa: E501
    )
    op.execute(
        """INSERT INTO task_type (created, modified, name, description) VALUES (now(), now(), 'Evidence Collection', 'Collect and Prepare Evidence from Clients')"""    # noqa: E501
    )
    op.execute(
        """INSERT INTO hearing_type (created, modified, name, description) VALUES (now(), now(), 'MASTER', 'Master Hearing')"""     # noqa: E501
    )
    op.execute(
        """INSERT INTO hearing_type (created, modified, name, description) VALUES (now(), now(), 'MERIT', 'Merit Hearing')"""    # noqa: E501
    )
    op.execute(
        """INSERT INTO form_type (created, modified, name, description) VALUES (now(), now(), 'I-589', 'Application for Asylum and for Withholding of Removal')"""  # noqa: E501
    )
    op.execute(
        """INSERT INTO form_type (created, modified, name, description) VALUES (now(), now(), 'I-765', 'Application for Employment Authorization')"""  # noqa: E501
    )
    op.execute(
        """INSERT INTO collection_method (created, modified, name, description) VALUES (now(), now(), 'Zelle', 'Paid via Zelle Transfer')"""  # noqa: E501
    )
    op.execute(
        """INSERT INTO collection_method (created, modified, name, description) VALUES (now(), now(), 'Money Order', 'Paid with Money Order')"""   # noqa: E501
    )
    op.execute(
        """INSERT INTO collection_method (created, modified, name, description) VALUES (now(), now(), 'Check', 'Paid with Personal Check')"""    # noqa: E501
    )
    op.execute(
        """INSERT INTO collection_method (created, modified, name, description) VALUES (now(), now(), 'Cash', 'Paid with Cash')"""  # noqa: E501
    )
    op.execute(
        """INSERT INTO case_type (created, modified, name, description) VALUES (now(), now(), 'Asylum', 'Filing for Asylum with USCIS or BIA')""" # noqa: E501
    )
    op.execute(
        """CREATE UNIQUE INDEX task_calendar_hearing_calendar_id_1 ON task_calendar (hearing_calendar_id) WHERE hearing_calendar_id IS NOT NULL"""  # noqa: E501
    )
    op.execute(
        """CREATE UNIQUE INDEX task_calendar_form_id_1 ON task_calendar (form_id) WHERE form_id IS NOT NULL"""  # noqa: E501
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("history_court_court_id", "history_court")
    op.drop_constraint("judge_court_id", "judge")
    op.drop_constraint("client_judge_id", "client")
    op.drop_constraint("history_judge_judge_id", "history_judge")
    op.drop_constraint("history_judge_court_id", "history_judge")
    op.drop_constraint("court_case_client_id", "court_case")
    op.drop_constraint("court_case_case_type_id", "court_case")
    op.drop_constraint("history_client_judge_id", "history_client")
    op.drop_constraint("history_client_client_id", "history_client")
    op.drop_constraint("case_collection_court_case_id", "case_collection")
    op.drop_constraint("form_form_type_id", "form")
    op.drop_constraint("form_court_case_id", "form")
    op.drop_constraint("hearing_calendar_hearing_type_id", "hearing_calendar")
    op.drop_constraint("hearing_calendar_court_case_id", "hearing_calendar")
    op.drop_constraint("history_court_case_court_case_id", "history_court_case")
    op.drop_constraint("history_court_case_client_id", "history_court_case")
    op.drop_constraint("history_court_case_case_type_id", "history_court_case")
    op.drop_constraint("cash_collection_collection_method_id", "cash_collection")
    op.drop_constraint("cash_collection_case_collection_id", "cash_collection")
    op.drop_constraint(
        "history_case_collection_case_collection_id", "history_case_collection"
    )
    op.drop_constraint(
        "history_case_collection_court_case_id", "history_case_collection"
    )
    op.drop_constraint(
        "history_hearing_calendar_hearing_type_id", "history_hearing_calendar"
    )
    op.drop_constraint(
        "history_hearing_calendar_hearing_calendar_id", "history_hearing_calendar"
    )
    op.drop_constraint(
        "history_hearing_calendar_court_case_id", "history_hearing_calendar"
    )
    op.drop_constraint("task_calendar_task_type_id", "task_calendar")
    op.drop_constraint("task_calendar_hearing_calendar_id", "task_calendar")
    op.drop_constraint("task_calendar_form_id", "task_calendar")
    # op.drop_constraint("task_calendar_hearing_calendar_id_1", "task_calendar")
    # op.drop_constraint("task_calendar_form_id_1", "task_calendar")
    op.drop_constraint(
        "history_cash_collection_case_collection_id", "history_cash_collection"
    )
    op.drop_constraint(
        "history_cash_collection_cash_collection_id", "history_cash_collection"
    )
    op.drop_constraint(
        "history_cash_collection_collection_method_id", "history_cash_collection"
    )
    op.drop_constraint("history_form_task_calendar_id", "history_form")
    op.drop_constraint("history_form_form_type_id", "history_form")
    op.drop_constraint("history_form_form_id", "history_form")
    op.drop_constraint("history_form_court_case_id", "history_form")
    op.drop_constraint("history_task_calendar_task_type_id", "history_task_calendar")
    op.drop_constraint(
        "history_task_calendar_task_calendar_id", "history_task_calendar"
    )
    op.drop_constraint(
        "history_task_calendar_hearing_calendar_id", "history_task_calendar"
    )
    op.drop_constraint("history_task_calendar_form_id", "history_task_calendar")
    op.drop_table("history_task_calendar")
    op.drop_table("history_form")
    op.drop_table("history_cash_collection")
    op.drop_table("task_calendar")
    op.drop_table("history_hearing_calendar")
    op.drop_table("history_case_collection")
    op.drop_table("cash_collection")
    op.drop_table("history_court_case")
    op.drop_table("hearing_calendar")
    op.drop_table("form")
    op.drop_table("case_collection")
    op.drop_table("history_client")
    op.drop_table("court_case")
    op.drop_table("history_judge")
    op.drop_table("client")
    op.drop_table("judge")
    op.drop_table("history_court")
    op.drop_table("task_type")
    op.drop_table("hearing_type")
    op.drop_table("form_type")
    op.drop_table("court")
    op.drop_table("collection_method")
    op.drop_table("case_type")
    # ### end Alembic commands ###
