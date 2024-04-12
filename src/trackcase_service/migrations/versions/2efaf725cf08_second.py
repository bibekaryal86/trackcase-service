"""second

Revision ID: 2efaf725cf08
Revises: e8011800626b
Create Date: 2024-04-12 12:18:50.773215

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "2efaf725cf08"
down_revision: Union[str, None] = "e8011800626b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "filing_rfe",
        sa.Column("filing_id", sa.Integer(), nullable=False),
        sa.Column("rfe_date", sa.DateTime(), nullable=False),
        sa.Column("rfe_submit_date", sa.DateTime(), nullable=True),
        sa.Column("rfe_reason", sa.String(length=3000), nullable=True),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_date", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["filing_id"],
            ["filing.id"],
            name="filing_rfe_filing_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "history_filing_rfe",
        sa.Column("app_user_id", sa.Integer(), nullable=False),
        sa.Column("filing_rfe_id", sa.Integer(), nullable=False),
        sa.Column("filing_id", sa.Integer(), nullable=False),
        sa.Column("rfe_date", sa.DateTime(), nullable=True),
        sa.Column("rfe_submit_date", sa.DateTime(), nullable=True),
        sa.Column("rfe_reason", sa.String(length=3000), nullable=True),
        sa.Column("comments", sa.String(length=10000), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_date", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["app_user_id"],
            ["app_user.id"],
            name="history_filing_rfe_app_user_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["filing_id"],
            ["filing.id"],
            name="history_filing_rfe_filing_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["filing_rfe_id"],
            ["filing_rfe.id"],
            name="history_filing_rfe_filing_rfe_id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_unique_constraint(
        "app_role_permission_ids",
        "app_role_permission",
        ["app_role_id", "app_permission_id"],
    )
    op.create_unique_constraint(
        "app_user_role_ids", "app_user_role", ["app_user_id", "app_role_id"]
    )
    op.create_unique_constraint(
        "court_case_case_type_client_id", "court_case", ["case_type_id", "client_id"]
    )
    op.drop_column("filing", "rfe_date")
    op.drop_column("filing", "rfe_submit_date")
    op.drop_column("history_filing", "rfe_date")
    op.drop_column("history_filing", "rfe_submit_date")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "history_filing",
        sa.Column(
            "rfe_submit_date",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "history_filing",
        sa.Column(
            "rfe_date", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "filing",
        sa.Column(
            "rfe_submit_date",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "filing",
        sa.Column(
            "rfe_date", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
    )
    op.drop_constraint("court_case_case_type_client_id", "court_case", type_="unique")
    op.drop_constraint("app_user_role_ids", "app_user_role", type_="unique")
    op.drop_constraint("app_role_permission_ids", "app_role_permission", type_="unique")
    op.drop_table("history_filing_rfe")
    op.drop_table("filing_rfe")
    # ### end Alembic commands ###
