import pytest

from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script, ScriptDirectory


@pytest.fixture()
def alembic_config():
    return Config(file_="alembic.ini", ini_section="alembic")


def get_revisions():
    config = Config(file_="alembic.ini", ini_section="alembic")

    revisions_dir = ScriptDirectory.from_config(config)

    revisions = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions


@pytest.mark.parametrize("revision", get_revisions())
def test_migrations_stairway(alembic_config: Config, revision: Script):
    upgrade(alembic_config, revision.revision)

    downgrade(alembic_config, revision.down_revision or "-1")
    upgrade(alembic_config, revision.revision)
