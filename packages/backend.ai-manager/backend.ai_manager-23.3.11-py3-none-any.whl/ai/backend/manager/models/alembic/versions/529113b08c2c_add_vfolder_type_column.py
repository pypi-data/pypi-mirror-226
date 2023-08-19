"""add_vfolder_type_column

Revision ID: 529113b08c2c
Revises: c481d3dc6c7d
Create Date: 2020-04-09 16:37:35.460936

"""
import textwrap

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import bindparam

from ai.backend.common.types import VFolderUsageMode
from ai.backend.manager.models import VFolderOwnershipType, VFolderPermission
from ai.backend.manager.models.base import GUID, EnumValueType, IDColumn, convention

# revision identifiers, used by Alembic.
revision = "529113b08c2c"
down_revision = "c481d3dc6c7d"
branch_labels = None
depends_on = None

vfperm_choices = list(map(lambda v: v.value, VFolderPermission))
# vfolderpermission type should already be defined.

vfusagemode_choices = list(map(lambda v: v.value, VFolderUsageMode))
vfolderusagemode = postgresql.ENUM(
    *vfusagemode_choices,
    name="vfolderusagemode",
)

vfownershiptype_choices = list(map(lambda v: v.value, VFolderOwnershipType))
vfolderownershiptype = postgresql.ENUM(
    *vfownershiptype_choices,
    name="vfolderownershiptype",
)


def upgrade():
    metadata = sa.MetaData(naming_convention=convention)
    # partial table to be preserved and referred
    vfolders = sa.Table(
        "vfolders",
        metadata,
        IDColumn("id"),
        sa.Column("ownership_type", EnumValueType(VFolderOwnershipType), nullable=False),
        sa.Column("user", GUID, sa.ForeignKey("users.uuid"), nullable=True),
        sa.Column("group", GUID, sa.ForeignKey("groups.id"), nullable=True),
    )

    vfolderusagemode.create(op.get_bind())
    vfolderownershiptype.create(op.get_bind())
    op.add_column(
        "vfolder_invitations",
        sa.Column(
            "modified_at",
            sa.DateTime(timezone=True),
            nullable=True,
            onupdate=sa.func.current_timestamp(),
        ),
    )
    op.add_column(
        "vfolders",
        sa.Column(
            "usage_mode", sa.Enum(*vfusagemode_choices, name="vfolderusagemode"), nullable=True
        ),
    )
    op.add_column(
        "vfolders",
        sa.Column(
            "ownership_type",
            sa.Enum(*vfownershiptype_choices, name="vfolderownershiptype"),
            nullable=True,
        ),
    )
    op.add_column(
        "vfolders",
        sa.Column("permission", sa.Enum(*vfperm_choices, name="vfolderpermission"), nullable=True),
    )

    # Fill vfolders.c.usage_mode with 'general' and vfolders.c.permission.
    conn = op.get_bind()
    query = textwrap.dedent("UPDATE vfolders SET usage_mode = 'general';")
    conn.execute(text(query))
    query = textwrap.dedent("UPDATE vfolders SET permission = 'wd' WHERE \"user\" IS NOT NULL;")
    conn.execute(text(query))
    query = textwrap.dedent("UPDATE vfolders SET permission = 'rw' WHERE \"group\" IS NOT NULL;")
    conn.execute(text(query))

    # Set vfolders.c.ownership_type field based on user and group column.
    query = sa.select([vfolders.c.id, vfolders.c.user, vfolders.c.group]).select_from(vfolders)
    updates = []
    for row in conn.execute(query).fetchall():
        if row["group"]:
            ownership_type = VFolderOwnershipType.GROUP
        else:
            ownership_type = VFolderOwnershipType.USER
        updates.append({"vfid": row["id"], "otype": ownership_type})
    if updates:
        query = (
            sa.update(vfolders)
            .values(ownership_type=bindparam("otype"))
            .where(vfolders.c.id == bindparam("vfid"))
        )
        conn.execute(query, updates)

    # Create indexes for name.
    op.create_index(op.f("ix_vfolders_name"), "vfolders", ["name"], unique=False)

    # Constraints
    op.create_check_constraint(
        "ownership_type_match_with_user_or_group",
        "vfolders",
        "(ownership_type = 'user' AND \"user\" IS NOT NULL) OR "
        "(ownership_type = 'group' AND \"group\" IS NOT NULL)",
    )
    op.create_check_constraint(
        "either_one_of_user_or_group",
        "vfolders",
        '("user" IS NULL AND "group" IS NOT NULL) OR ("user" IS NOT NULL AND "group" IS NULL)',
    )

    op.alter_column("vfolders", column_name="usage_mode", nullable=False)
    op.alter_column("vfolders", column_name="permission", nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("ck_vfolders_ownership_type_match_with_user_or_group", "vfolders")
    op.drop_constraint("ck_vfolders_either_one_of_user_or_group", "vfolders")
    op.drop_index(op.f("ix_vfolders_name"), table_name="vfolders")
    op.drop_column("vfolders", "usage_mode")
    op.drop_column("vfolders", "ownership_type")
    op.drop_column("vfolders", "permission")
    op.drop_column("vfolder_invitations", "modified_at")
    vfolderusagemode.drop(op.get_bind())
    vfolderownershiptype.drop(op.get_bind())
    # ### end Alembic commands ###
