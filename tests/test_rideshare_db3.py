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

        createUser('Godot', 'None', 3.2, None, 10301, datetime.datetime.now().isoformat(' ', 'seconds'), False, False, None, True, False, 'Toyota', 'Rav4', 378129321)
        markAvailableDriver(4, 10301)
        createUser('Vladamir', 'None', 2.4, None, 10301, datetime.datetime.now().isoformat(' ', 'seconds'), True, True, 637821321, False, False, None, None, None)
        createUser('Alex Reger', 'None', 4.2, None, 32193, datetime.date(1979, 9, 1), True, False, 73892132, True, True, 'Make', 'Model', 32617831)
        createUser('Bobby Wheeler', 'None', 4.7, None, 32193, datetime.date(2001, 11, 1), True, True, 32671893, True, False, 'Make', 'Model', 789792132)
        createUser('Louie DePalma', 'None', 3.8, None, 32193, datetime.date(1979, 9, 3), True, True, 89321867, True, False, 'Make', 'Model', 432893212)
        createUser('Elaine Nardo', 'None', 4.0, None, 32193, datetime.date(1980, 9, 5), True, True, 43876432, True, False, 'Make', 'Model', 790732123)
        createUser('Tony Banta', 'None', 3.4, None, 32193, datetime.date(1980, 10, 1), True, True, 78543234, True, False, 'Make', 'Model', 890893212)
        startRide(6, 7, 12, None, '(5, 12)')
        joinRide(6, 8, '(5, 12)')
        joinRide(6, 9, '(5, 12)')
        joinRide(6, 10, '(5, 12)')
        writeReview(8, 4, 2, 'Bad Review')
        writeReview(7, 4, 5, 'Good Review')
        respondToReview(1, 'Shut up')
        markAvailableRider(6, 32193)
        markAvailableDriver(10, 32193)
        startRide(10, 6, 10, None, '(12, 8)')
        joinRide(10, 9, '(12, 8)')
        markUnavailableDriver(10)
        updateDayHappened(4, datetime.datetime(2024, 2, 21, 12, 15))
        updateDayHappened(5, datetime.datetime(2024, 2, 21, 12, 15))
        

    def test_godot_available(self):
        data = isAvailableDriver(4)
        self.assertTrue(data)
        
    def test_godot_reciept(self):
        data = getReceipt(4, datetime.datetime(2023, 2, 21, 12, 15), datetime.datetime(2025, 2, 21, 12, 15))
        self.assertEqual(data, [])

    def test_alex_riders(self):
        data = getRiders(6, '(5, 12)')
        self.assertEqual(data, [('Bobby Wheeler',), ('Louie DePalma',), ('Elaine Nardo',), ('Tony Banta',)])

    def test_bobby_receipt(self):
        data = getReceipt(7, datetime.datetime(2023, 2, 21, 12, 15), datetime.datetime(2025, 2, 21, 12, 15))
        self.assertEqual(data, [3])

    def test_louie_review(self):
        data = getReview(6, 8)
        self.assertEqual(data, (2, 'Bad Review'))

    def test_bobby_review(self):
        data = getReview(6, 7)
        self.assertEqual(data, (5, 'Good Review'))

    def test_alex_respond(self):
        data = getResponse(6, 8)
        self.assertEqual(data, ('Shut up',))

    def test_tony_unavailable(self):
        data = getAvailableDrivers(32193)
        self.assertEqual(data, [])

    def test_additional_1(self):
        """Tests for multiple receipts"""
        data = getReceipt(9, datetime.datetime(2023, 2, 21, 12, 15), datetime.datetime(2025, 2, 21, 12, 15))
        self.assertEqual(data, [3, 5])

    def test_additional_2(self):
        """Tests getAvailableRiders function"""
        data = getAvailableRiders(32193)
        self.assertEqual(data, [('Bobby Wheeler',), ('Louie DePalma',), ('Elaine Nardo',), ('Alex Reger',)])

    def test_additional_3(self):
        """Tests getAvailableDrivers with someone available"""
        markAvailableDriver(10, 32193)
        data = getAvailableDrivers(32193)
        self.assertEqual(data, [('Tony Banta',)])


    def test_db4_1(self):
        """Gets full ride info"""
        data = getFullRideInfo(datetime.datetime(2023, 2, 21, 12, 15), datetime.datetime(2025, 2, 21, 12, 15))
        equal = ['Alex Reger', ('(5,12)',), [('Bobby Wheeler',), ('Louie DePalma',), ('Elaine Nardo',), ('Tony Banta',)], 3.5, 
                    'Tony Banta', ('(12,8)',), [('Alex Reger',), ('Elaine Nardo',)], 0]
        self.assertEqual(data, equal)

    def test_db4_2(self):
        """Gets fare times and prices"""
        data = getFareTimes()
        self.assertEqual(data, [12, 11.0])