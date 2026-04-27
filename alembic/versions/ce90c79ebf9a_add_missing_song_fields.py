"""add_missing_song_fields

Revision ID: ce90c79ebf9a
Revises: c9cb8f4b082e
Create Date: 2026-04-27 21:51:42.319409

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "ce90c79ebf9a"
down_revision: Union[str, Sequence[str], None] = "c9cb8f4b082e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Handle the CockroachDB/Postgres Enum Type manually
    # checkfirst=True prevents errors if the type already exists
    user_role_enum = sa.Enum("user", "admin", name="user_role_enum")
    user_role_enum.create(op.get_bind(), checkfirst=True)

    # 2. Update favorite_songs table
    op.alter_column(
        "favorite_songs",
        "song_id",
        existing_type=sa.VARCHAR(),
        type_=sa.Text(),
        existing_nullable=False,
    )
    op.drop_index(
        op.f("ix_favorite_songs_song_id"),
        table_name="favorite_songs",
        postgresql_ops={"song_id": None},
        postgresql_using="prefix",
    )
    op.create_index(
        op.f("ix_favorite_songs_song_id"), "favorite_songs", ["song_id"], unique=False
    )

    # 3. Update songs table (Adding the missing fields)
    op.add_column(
        "songs",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "songs",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.alter_column(
        "songs",
        "song_id",
        existing_type=sa.VARCHAR(),
        type_=sa.TEXT(),
        existing_nullable=False,
    )

    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.VARCHAR(),
        type_=sa.Text(),
        existing_nullable=False,
    )

    # Standardize email index
    op.drop_constraint(op.f("ix_users_email"), "users", type_="unique")
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Revert user table changes
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.create_unique_constraint(
        op.f("ix_users_email"), "users", ["email"], postgresql_nulls_not_distinct=False
    )
    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.Text(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.drop_column("users", "role")

    # 2. Revert song table changes
    op.alter_column(
        "songs",
        "song_id",
        existing_type=sa.TEXT(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.drop_column("songs", "updated_at")
    op.drop_column("songs", "created_at")

    # 3. Revert favorite_songs table changes
    op.drop_index(op.f("ix_favorite_songs_song_id"), table_name="favorite_songs")
    op.create_index(
        op.f("ix_favorite_songs_song_id"),
        "favorite_songs",
        [sa.literal_column("song_id NULLS FIRST")],
        unique=False,
        postgresql_ops={"song_id": None},
        postgresql_using="prefix",
    )
    op.alter_column(
        "favorite_songs",
        "song_id",
        existing_type=sa.Text(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )

    # 4. Remove the Enum type
    sa.Enum(name="user_role_enum").drop(op.get_bind(), checkfirst=True)
