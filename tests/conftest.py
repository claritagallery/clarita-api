import pytest

from clarita.config import Settings
from clarita.digikam.db import DigikamSQLite


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def digikam(settings):
    digikam = DigikamSQLite(settings.database_main_path, settings.root_map)
    yield digikam
    await digikam.close()


@pytest.fixture(scope="session")
def settings():
    return Settings()
