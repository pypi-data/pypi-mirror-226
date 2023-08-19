"""add_images_col_to_session

Revision ID: eb9441fcf90a
Revises: 69c059996cbd
Create Date: 2023-07-06 13:51:52.098587

"""
from collections import defaultdict

import sqlalchemy as sa
from alembic import op
from sqlalchemy.orm import registry
from sqlalchemy.sql.expression import bindparam

from ai.backend.manager.models.base import GUID, convention

# revision identifiers, used by Alembic.
revision = "eb9441fcf90a"
down_revision = "69c059996cbd"
branch_labels = None
depends_on = None

metadata = sa.MetaData(naming_convention=convention)
mapper_registry = registry(metadata=metadata)
Base = mapper_registry.generate_base()

PAGE_SIZE = 100
DEFAULT_ROLE = "main"


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    op.add_column("sessions", sa.Column("images", sa.ARRAY(sa.String()), nullable=True))
    kernels = sa.Table(
        "kernels",
        metadata,
        sa.Column("id", GUID, primary_key=True),
        sa.Column("session_id", GUID, nullable=False),
        sa.Column("image", sa.String(length=512)),
        sa.Column(
            "cluster_role",
            sa.String(length=16),
        ),
    )

    class SessionRow(Base):  # type: ignore[valid-type, misc]
        __tablename__ = "sessions"
        id = sa.Column(
            "id",
            GUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
            primary_key=True,
        )
        images = sa.Column("images", sa.ARRAY(sa.String), nullable=True)

    kernel_cnt = conn.execute(sa.select([sa.func.count()]).select_from(kernels)).scalar()

    for offset in range(0, kernel_cnt, PAGE_SIZE):
        session_agent_ids_map = defaultdict(list)
        session_id_query = (
            sa.select([sa.distinct(kernels.c.session_id)])
            .where(kernels.c.image.is_not(None))
            .order_by(kernels.c.session_id)
            .offset(offset)
            .limit(PAGE_SIZE)
        )
        session_ids = conn.execute(session_id_query).scalars().all()
        stmt = sa.select([kernels]).where(kernels.c.session_id.in_(session_ids))
        kernel_rows = conn.execute(stmt).fetchall()
        for row in kernel_rows:
            img_list = session_agent_ids_map[row["session_id"]]
            if row["image"] in img_list:
                continue
            if row["cluster_role"] == DEFAULT_ROLE:
                img_list.insert(0, row["image"])
            else:
                img_list.append(row["image"])
        if session_agent_ids_map:
            conn.execute(
                sa.update(SessionRow)
                .values({"images": bindparam("images")})
                .where(SessionRow.id == bindparam("b_session_id")),
                [
                    {
                        "b_session_id": session_id,
                        "images": list(images),
                    }
                    for session_id, images in session_agent_ids_map.items()
                ],
            )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("sessions", "images")
    # ### end Alembic commands ###
