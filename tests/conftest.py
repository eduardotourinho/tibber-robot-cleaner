import pytest
from dotenv import load_dotenv

from cleanerrobot.adapters.storage.db import initialize_db, get_db_config, drop_all_tables

load_dotenv()


@pytest.fixture(scope="module")
def db_engine():
    engine = initialize_db(get_db_config())
    yield engine
    drop_all_tables(engine)
