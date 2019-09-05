from datetime import datetime

import pytest

from apps import create_app
from core.settings import TestingConfig


@pytest.fixture
async def app():
    app = create_app(config=TestingConfig)
    yield app


@pytest.fixture
def current_time():
    return datetime.utcnow().replace(microsecond=0)
