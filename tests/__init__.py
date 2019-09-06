from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from core.settings import get_config

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


@pytest.yield_fixture
def session():
    engine = create_engine(get_config().db_url)
    db_session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
        )
    )
    yield db_session
    db_session.rollback()
    db_session.remove()
