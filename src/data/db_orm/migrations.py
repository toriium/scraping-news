from alembic.config import Config
from alembic import command

from src.settings import BASE_DIR


def run_migrations() -> None:
    print('Running DB migrations')
    alembic_cfg = Config(f'{BASE_DIR}/alembic.ini')
    alembic_cfg.set_main_option('script_location', f'{BASE_DIR}/src/data/db_orm/alembic')

    command.upgrade(alembic_cfg, 'head')
