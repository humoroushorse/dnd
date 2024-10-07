"""${message}.

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: str | None = ${repr(down_revision)}
branch_labels: str | Sequence[str] | None = ${repr(branch_labels)}
depends_on: str | Sequence[str] | None = ${repr(depends_on)}


def upgrade():
    """Database migration: upgrade."""
    pre_upgrade()

    ${upgrades if upgrades else "pass"}

    post_upgrade()


def downgrade():
    """Database migration: downgrade."""
    pre_downgrade()

    ${downgrades if downgrades else "pass"}

    post_downgrade()


def pre_upgrade():
    """Processing before upgrading the schema."""
    pass


def post_upgrade():
    """Processing after upgrading the schema."""
    pass


def pre_downgrade():
    """Processing before downgrading the schema."""
    pass


def post_downgrade():
    """Processing after downgrading the schema."""
    pass
