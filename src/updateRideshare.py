from src.rideshare import *
from src.getRideshare import *
from src.swen344_db_utils import *

def updateName(name, id):
    """Updates the user's name"""
    exec_commit('''UPDATE users SET name = %s WHERE id = %s''', [name, id])

def updateInstructions(instructions, id):
    """Updates the user's instructions"""
    exec_commit('''UPDATE users SET instructions = %s WHERE id = %s''', [instructions, id])

def updateLocation(location, id):
    """Updates the user's location"""
    exec_commit('''UPDATE users SET location = %s WHERE id = %s''', [location, id])

def markAvailableRider(id, zipcode):
    """Marks the user available as a rider and sets their zipcode to their current zipcode"""
    exec_commit('''UPDATE users SET available_rider = TRUE WHERE id = %s''', [id])
    exec_commit('''UPDATE users SET zipcode = %s WHERE id = %s''', [zipcode, id])
    markUnavailableDriver(id)

def markAvailableDriver(id, zipcode):
    """Marks the user available as a driver and sets their zipcode to their current zipcode"""
    exec_commit('''UPDATE users SET available_driver = TRUE WHERE id = %s''', [id])
    exec_commit('''UPDATE users SET zipcode = %s WHERE id = %s''', [zipcode, id])
    markUnavailableRider(id)

def markUnavailableRider(id):
    """Marks the user unavailable as a rider"""
    exec_commit('''UPDATE users SET available_rider = FALSE WHERE id = %s''', [id])

def markUnavailableDriver(id):
    """Marks the user unavailable as a driver"""
    exec_commit('''UPDATE users SET available_driver = FALSE WHERE id = %s''', [id])

def makeRider(number, id):
    """Sets the user as a rider"""
    exec_commit('''UPDATE users SET rider = TRUE WHERE id = %s''', [id])
    updateCreditCard(number, id)

def updateCreditCard(number, id):
    """Updates the user's credit card number"""
    exec_commit('''UPDATE users SET credit_card_num = %s WHERE id = %s''', [number, id])

def makeDriver(make, model, number, id):
    """Sets the user as a rider"""
    exec_commit('''UPDATE users SET driver = TRUE WHERE id = %s''', [id])
    updateCarMake(make, id)
    updateCarModel(model, id)
    updateLicenseNum(number, id)

def updateCarMake(make, id):
    """Updates the user's car make"""
    exec_commit('''UPDATE users SET car_make = %s WHERE id = %s''', [make, id])
    
def updateCarModel(model, id):
    """Updates the user's car model"""
    exec_commit('''UPDATE users SET car_model = %s WHERE id = %s''', [model, id])

def updateLicenseNum(number, id):
    """Updates the user's license number"""
    exec_commit('''UPDATE users SET license_num = %s WHERE id = %s''', [number, id])

def updateDayHappened(ride, day):
    """Updates the day a ride happened"""
    exec_commit('''UPDATE rides SET day_happened = %s WHERE id = %s''', [day, ride])