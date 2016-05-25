import unittest

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy_utils import database_exists, create_database

from models import Base


def setup_module():
    global transaction, connection, engine

    # Connect to the database and create the schema within a transaction
    engine = create_engine('postgresql://localhost/test', echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    connection = engine.connect()
    transaction = connection.begin()
    Base.metadata.create_all(connection)


def teardown_module():
    # Roll back the top level transaction and disconnect from the database
    transaction.rollback()
    connection.close()
    engine.dispose()


class DatabaseTest(object):
    def setup(self):
        self.__transaction = connection.begin_nested()
        self.session = Session(connection)

    def teardown(self):
        self.session.close()
        self.__transaction.rollback()


class TestModels(DatabaseTest, unittest.TestCase):
    def setup(self):
        super().setup()

    def teardown(self):
        super().teardown()

    def test_somth(self):
        a = 5
        self.assertEqual(a, 5)

if __name__ == "__main__":
    setup_module()
    unittest.main()
    teardown_module()
