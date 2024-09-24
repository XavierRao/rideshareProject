import datetime
import unittest
from src.rideshare import *
from src.getRideshare import *
from src.updateRideshare import *
from src.swen344_db_utils import *

class TestRideshare(unittest.TestCase):

    def setUp(self):
        rebuildTables()
        fillTables()

        createUser('Hoke Colburn', 'Always in a rush', 3.3, None, None, datetime.date(1989, 12, 2), False, False, None, True, True, 'Make', 'Model', '234567890')
        createUser('Ms. Daisy', 'Take it easy', 4.5, None, None, datetime.date(1989, 12, 2), True, False, 2345678901234567, False, False, None, None, None)
        markAvailableRider(5, 30301)
        startRide(4, 5, None, None, None)
        updateDayHappened(4, datetime.date(1989, 12, 13))
        
        makeRider(4, 345678901234567)
        startRide(2, 4, None, None, None)
        updateDayHappened(5, datetime.date(1989, 12, 14))
        startRide(3, 4, None, None, None)
        updateLicenseNum('345678901', 4)

    def test_tom_update(self):
        """Check Tom's update"""
        updateCarModel('Corolla', 2)
        self.assertEqual(getCarModel(2), ('Corolla',))
    
    def test_ray_update(self):
        """Check Ray's update"""
        updateInstructions('Fast over slow', 3)
        self.assertEqual(getInstructions(3), ('Fast over slow',))

    def test_hoke_create(self):
        """Check if Hoke is a user"""
        data = getName(4)
        self.assertEqual(data, ('Hoke Colburn',))

    def test_daisy_create(self):
        """Check if Ms. Daisy is a user"""
        data = getName(5)
        self.assertEqual(data, ('Ms. Daisy',))

    def test_daisy_available(self):
        data = isAvailableRider(5)
        self.assertTrue(data)

    def test_hoke_available_riders(self):
        data = getAvailableRiders(30301)
        self.assertEqual(data, [('Ms. Daisy',)])

    def test_hoke_drive_daisy(self):
        data = getRide(4, 5)
        self.assertEqual(data, (datetime.datetime(1989, 12, 13, 0, 0),))

    def test_tom_drive_hoke(self):
        data = getRide(2, 4)
        self.assertEqual(data, (datetime.datetime(1989, 12, 14, 0, 0),))

    def test_daisy_remove(self):
        removeAccount(5)
        data = getName(5)
        self.assertEqual(data, None)

    def test_rides_hoke_took(self):
        data = getRidesTaken(4)
        self.assertEqual(data, [('Tom Magliozzi',), ('Ray Magliozzi',)])

    def test_hoke_location(self):
        data = getLocation(4)
        self.assertTrue(data, (0, 0))

    def test_hoke_update(self):
        data = getLicenseNum(4)
        self.assertEqual(data, ('345678901',))