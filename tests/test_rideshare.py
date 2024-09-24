import csv
import unittest
from src.rideshare import *
from src.getRideshare import *
from src.updateRideshare import *
from src.swen344_db_utils import *

class TestRideshare(unittest.TestCase):

    def setUp(self):
        rebuildTables()
        fillTables()

    def test_rebuild_tables(self):
        """Build the tables"""
        rebuildTables()
        users = exec_get_all('SELECT * FROM users')
        self.assertEqual([], users, "no rows in users")
        rides = exec_get_all('SELECT * FROM rides')
        self.assertEqual([], rides, "no rows in rides")

    def test_rides_tom_gave(self):
        """Check the rides Tom gave"""
        data = getRidesGiven(2)
        self.assertEqual(data, [('Mike Easter',), ('Ray Magliozzi',)])

    def test_rides_mike_gave(self):
        """Check the rides Mike gave"""
        data = getRidesGiven(1)
        self.assertEqual(data, [])
    
    def test_ride_mike_took(self):
        """Check the rides Mike took"""
        data = getRidesTaken(1)
        self.assertEqual(data, [('Tom Magliozzi',), ('Ray Magliozzi',)])

    def test_rides_ray_took(self):
        """Check the rides Ray took"""
        data = getRidesTaken(3)
        self.assertEqual(data, [('Tom Magliozzi',)])

    def test_tom_rating(self):
        """Check Tom's rating"""
        data = getRating(2)
        self.assertTrue(data, 3.2)

    def test_ray_rating(self):
        """Check Ray's rating"""
        data = getRating(3)
        self.assertTrue(data, 3.4)

    def test_mike_rating(self):
        """Check Mike's rating"""
        data = getRating(1)
        self.assertTrue(data, 4.3)

    def test_a(self):
        print(exec_get_all('SELECT * FROM users'))