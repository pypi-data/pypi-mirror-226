"""add superadmin role for user

Revision ID: e18ed5fcfedf
Revises: c5e4e764f9e3
Create Date: 2019-05-29 23:17:17.762968

"""
import textwrap

from alembic import op
from sqlalchemy.sql import text

from ai.backend.manager.models import UserRole

# revision identifiers, used by Alembic.
revision = "e18ed5fcfedf"
down_revision = "c5e4e764f9e3"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

    # Add superadmin to user role choices.
    userrole_choices = list(map(lambda v: v.value, UserRole))
    assert "superadmin" in userrole_choices, "superadmin in UserRole is required!"

    conn = op.get_bind()
    conn.execute(text("ALTER TYPE userrole RENAME TO userrole__;"))
    conn.execute(
        text("CREATE TYPE userrole as enum (%s)" % ("'" + "','".join(userrole_choices) + "'"))
    )
    conn.execute(text(textwrap.dedent("""\
        ALTER TABLE users
            ALTER COLUMN role TYPE userrole USING role::text::userrole;
    """)))
    conn.execute(text("DROP TYPE userrole__;"))

    # Set admin@lablup.com's role as superadmin.
    # Also, set admin@lablup.com's domain to default.
    #
    # We have judged superadmin as an admin user not associated with any domain.
    # This results in broken code execution for superadmin since doamain_name should not be null.
    # So, this policy is changed to simply adopt superadmin role, and superadmin can also have
    # domain and groups as well.
    query = "SELECT uuid FROM users where email = 'admin@lablup.com';"
    result = conn.execute(text(query)).first()
    uuid = result.uuid if hasattr(result, "uuid") else None
    if uuid is not None:  # update only when admin@lablup.com user exist
        query = textwrap.dedent("""\
            UPDATE users SET domain_name = 'default', role = 'superadmin'
            WHERE email = 'admin@lablup.com';
        """)
        conn.execute(text(query))


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

    userrole_choices = list(map(lambda v: v.value, UserRole))
    if "superadmin" in userrole_choices:
        userrole_choices.remove("superadmin")
        conn = op.get_bind()

        # First, change all superadmin role to admin.
        query = textwrap.dedent("UPDATE users SET role = 'admin' WHERE role = 'superadmin';")
        conn.execute(text(query))

        # Remove superadmin from user role choices.
        conn.execute(text("ALTER TYPE userrole RENAME TO userrole___;"))
        conn.execute(
            text("CREATE TYPE userrole as enum (%s)" % ("'" + "','".join(userrole_choices) + "'"))
        )
        conn.execute(text(textwrap.dedent("""\
            ALTER TABLE users
                ALTER COLUMN role TYPE userrole USING role::text::userrole;
        """)))
        conn.execute(text("DROP TYPE userrole___;"))
