"""Modified Report.used_music field

Revision ID: 4f941e4abcf2
Revises: 3f586067d50d
Create Date: 2025-03-12 17:26:13.877874

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "4f941e4abcf2"
down_revision: Union[str, None] = "3f586067d50d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "reports",
        sa.Column(
            "used_music",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default="[]",
            nullable=True,
        ),
    )
    op.drop_column("reports", "used_music_ids")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "reports",
        sa.Column(
            "used_music_ids",
            sa.TEXT(),
            server_default=sa.text("'[]'::text"),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column("reports", "used_music")
    # ### end Alembic commands ###
