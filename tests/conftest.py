import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///:memory:"

def _make_engine():
    # StaticPool keeps a single underlying connection so all sessions see the
    # same in-memory SQLite database (separate connections would each get a
    # fresh, empty database)
    return create_engine(
        TEST_DATABASE_URL,
        connect_args = {"check_same_thread": False},
        poolclass = StaticPool
    )

@pytest.fixture
def client():
    engine = _make_engine()
    Base.metadata.create_all(bind = engine)
    TestingSession = sessionmaker(autocommit = False, autoflush = False, bind = engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind = engine)
    engine.dispose()

@pytest.fixture
def db_session():
    engine = make_engine()
    Base.metadata.create_all(bind = engine)
    Session = sessionmaker(autocommit = False, autoflush = False, bind = engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind = engine)
        engine.dispose()