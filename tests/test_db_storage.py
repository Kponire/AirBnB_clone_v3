#!/usr/bin/python3
"""
Unittests for DBStorage class
"""
import unittest
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from os import getenv
import MySQLdb
import pep8
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.base_model import Base
from models.engine.db_storage import DBStorage


class TestDBStorage(unittest.TestCase):
    """
    Test the DBStorage class
    """
    @classmethod
    def setUpClass(cls):
        """ Set up for tests """
        cls.db = MySQLdb.connect(host=getenv('HBNB_MYSQL_HOST'),
                                user=getenv('HBNB_MYSQL_USER'),
                                passwd=getenv('HBNB_MYSQL_PWD'),
                                db=getenv('HBNB_MYSQL_DB'))
        cls.cur = cls.db.cursor()

        @classmethod
        def tearDownClass(cls):
            """ Remove test data and close connection """
            cls.cur.close()
            cls.db.close()

        def setUp(self):
            """ Set up for test """
            self.storage = DBStorage()

        def tearDown(self):
            """ Remove temporary file (if it exists) """
            self.storage.close()

        def test_pep8_DBStorage(self):
            """ Test for PEP-8 """
            pep8style = pep8.StyleGuide(quiet=True)
            result = pep8style.check_files(['models/engine/db_storage.py'])
            self.assertEqual(result.total_errors, 0, "PEP-8 style error(s) found")

        def test_docstring(self):
            """ Test for docstring """
            self.assertIsNotNone(DBStorage.__doc__)
            self.assertIsNotNone(DBStorage.all.__doc__)
            self.assertIsNotNone(DBStorage.new.__doc__)
            self.assertIsNotNone(DBStorage.save.__doc__)
            self.assertIsNotNone(DBStorage.delete.__doc__)
            self.assertIsNotNone(DBStorage.reload.__doc__)
            self.assertIsNotNone(DBStorage.get.__doc__)
            self.assertIsNotNone(DBStorage.count.__doc__)

        def test_attr(self):
            """ Test for attributes """
            self.assertTrue(hasattr(DBStorage, '_DBStorage__engine'))
            self.assertTrue(hasattr(DBStorage, '_DBStorage__session'))
            self.assertTrue(hasattr(DBStorage, 'all'))
            self.assertTrue(hasattr(DBStorage, 'new'))
            self.assertTrue(hasattr(DBStorage, 'save'))
            self.assertTrue(hasattr(DBStorage, 'delete'))
            self.assertTrue(hasattr(DBStorage, 'reload'))
            self.assertTrue(hasattr(DBStorage, 'get'))
            self.assertTrue(hasattr(DBStorage, 'count'))

        def test_empty(self):
            """ Test for empty """
            self.storage.reload()
            storage_all = storage.all()
            self.assertEqual(len(storage_all), 0)

        def test_get_set(self):
            """ Test for get and set """
            self.storage.reload()
            storage_all = storage.all()
            user = User()
            user.name = "Holberton"
            user.email = "airbnb@holbertonshool.com"
            user.password = "root"
            self.storage.new(user)
            self.storage.save()
            self.assertIn(user, storage_all.values())

        def test_count(self):
            """ Test for count """
            self.storage.reload()
            initial_count = len(self.storage.all())
            user = User()
            user.name = "Holberton"
            user.email = "airbnb@holbertonshool.com"
            user.password = "root"
            self.storage.new(user)
            self.storage.save()
            self.assertEqual(self.storage.count(), initial_count + 1)

if __name__ == "__main__":
    unittest.main()
