import pytest

from clarita.exceptions import DoesNotExist
from clarita.models import Root


async def test_root_detail(anyio_backend, digikam):
    assert await digikam.root_detail(1) == Root(
        id="1",
        label="Test images",
        status=0,
        type=1,
        specific_path="/home/fidel/Code/clarita-api/tests/images",
        case_sensitivity=2,
    )
    assert await digikam.root_detail(2) == Root(
        id="2",
        label="Smartphone",
        status=0,
        type=1,
        specific_path="/home/fidel/Downloads/Smartphone",
        case_sensitivity=2,
    )
    assert await digikam.root_detail(3) == Root(
        id="3",
        label="Clarita USB drive",
        status=0,
        type=1,
        specific_path="/var/run/media/fidel/FFBF-EEB3/Clarita",
        case_sensitivity=1,
    )
    with pytest.raises(DoesNotExist):
        await digikam.root_detail(4)


async def test_root_path(anyio_backend, digikam):
    assert await digikam.root_path(1) == "tests/images/"
    assert await digikam.root_path(2) == "/home/fidel/Downloads/Smartphone"
    assert await digikam.root_path(3) == "/var/run/media/fidel/FFBF-EEB3/Clarita"
    with pytest.raises(DoesNotExist):
        await digikam.root_path(4)
