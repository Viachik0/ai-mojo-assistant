import pytest
import sys
from unittest.mock import Mock, MagicMock

# Mock SQLAlchemy modules before any imports
mock_sa = MagicMock()
mock_sa.Column = MagicMock()
mock_sa.Integer = MagicMock()
mock_sa.String = MagicMock()
mock_sa.Float = MagicMock()
mock_sa.Boolean = MagicMock()
mock_sa.DateTime = MagicMock()
mock_sa.Text = MagicMock()
mock_sa.ForeignKey = MagicMock()
mock_sa.select = MagicMock()
mock_sa.func = MagicMock()
mock_sa.and_ = MagicMock()
mock_sa.or_ = MagicMock()

sys.modules['sqlalchemy'] = mock_sa

# Mock SQLAlchemy orm
mock_sa_orm = MagicMock()
mock_sa_orm.relationship = MagicMock()
mock_sa_orm.sessionmaker = MagicMock()
sys.modules['sqlalchemy.orm'] = mock_sa_orm

# Mock SQLAlchemy ext.asyncio
mock_sa_asyncio = MagicMock()
mock_sa_asyncio.create_async_engine = MagicMock()
mock_sa_asyncio.AsyncSession = MagicMock()
sys.modules['sqlalchemy.ext.asyncio'] = mock_sa_asyncio

# Mock declarative base
from unittest.mock import MagicMock as Base
mock_declarative_base = MagicMock(return_value=Base)
sys.modules['sqlalchemy.ext.declarative'] = MagicMock(declarative_base=mock_declarative_base)

# Mock the database module
mock_database = MagicMock()
mock_database.Base = Base
mock_database.engine = MagicMock()
mock_database.AsyncSession = MagicMock()
sys.modules['app.core.database'] = mock_database
