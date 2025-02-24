from alembic import context
from sqlalchemy import create_engine

from core.config import settings
from core.models import *

config = context.config

db_url = settings.db.get_url_sync()

target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=db_url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    engine = create_engine(
        url=db_url,
        echo=settings.db.echo,
        echo_pool=settings.db.echo_pool,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow
    )

    with engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
