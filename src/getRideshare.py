from src.rideshare import *
from src.updateRideshare import *
from src.swen344_db_utils import *

def getName(id):
    """Gets the user's name"""
    return exec_get_one('''SELECT name FROM users WHERE id = %s''', [id])

def getInstructions(id):
    """Gets the user's instructions"""
    return exec_get_one('''SELECT instructions FROM users WHERE id = %s''', [id])

def getRating(id):
    """Gets the user's rating"""
    return exec_get_one('''SELECT rating FROM users WHERE id = %s''', [id])

def getLocation(id):
    """Gets the user's location"""
    return exec_get_one('''SELECT location FROM users WHERE id = %s''', [id])

def getCreditCard(id):
    """Gets the user's credit card number"""
    return exec_get_one('''SELECT credit_card_num FROM users WHERE id = %s''', [id])

def isAvailableRider(id):
    """Checks if the rider is marked as available"""
    return exec_get_one('''SELECT available_rider FROM users WHERE id = %s''', [id])

def isAvailableDriver(id):
    """Checks if the driver is marked as available"""
    return exec_get_one('''SELECT available_driver FROM users WHERE id = %s''', [id])

def getCarMake(id):
    """Gets the user's car make"""
    return exec_get_one('''SELECT car_make FROM users WHERE id = %s''', [id])

def getCarModel(id):
    """Gets the user's car model"""
    return exec_get_one('''SELECT car_model FROM users WHERE id = %s''', [id])

def getLicenseNum(id):
    """Gets the user's license number"""
    return exec_get_one('''SELECT license_num FROM users WHERE id = %s''', [id])

def getRidesGiven(id):
    """Gets the riders the user has given a ride"""
    return exec_get_all('''SELECT name 
                            FROM users 
                                INNER JOIN passenger ON users.id = passenger.user_id
                                INNER JOIN rides ON passenger.id = rides.passenger_id
                            WHERE rides.driver = %s''', [id])

def getRidesTaken(id):
    """Gets the drivers the user has taken a ride from"""
    return exec_get_all('''SELECT name 
                            FROM users 
                                INNER JOIN rides ON users.id = rides.driver
                                INNER JOIN passenger ON rides.passenger_id = passenger.id
                            WHERE passenger.user_id = %s''', [id])

def getRide(driver, passenger):
    """Gets the day a specific ride happened"""
    return exec_get_one('''SELECT day_happened 
                            FROM rides
                                INNER JOIN passenger ON rides.passenger_id = passenger.id
                            WHERE driver = %s AND passenger.user_id = %s''', [driver, passenger])

def getRiders(driver, destination):
    """Gets the riders in the car of the current ride"""
    return exec_get_all('''SELECT name 
                            FROM users
                                INNER JOIN passenger ON users.id = passenger.user_id
                                INNER JOIN rides ON passenger.rides_id = rides.id
                            WHERE rides.driver = %s AND rides.destination ~= %s''', [driver, destination])

def getAvailableRiders(zipcode):
    """Gets the riders in the driver's zipcode"""
    return exec_get_all('''SELECT name FROM users WHERE zipcode = %s AND available_rider = TRUE''', [zipcode])

def getAvailableDrivers(zipcode):
    """Gets the drivers in the riders's zipcode"""
    return exec_get_all('''SELECT name FROM users WHERE zipcode = %s AND driver = TRUE AND available_driver = TRUE''', [zipcode])

def getAveragePrice(hour):
    """Get the price of rides for an hour"""
    prices = exec_get_all('''SELECT price FROM rides WHERE EXTRACT(HOUR FROM day_happened) = %s''', [hour])
    price = 0.0
    count = 0
    for p in prices:
        if (p[0] != None):
            price += p[0]
        count += 1
    return price/count

def getReceipt(user_id, start_date, end_date):
    """Gets the receipts for all the rides of a rider"""
    rides = exec_get_all('''SELECT rides_id 
                            FROM passenger 
                                INNER JOIN rides ON passenger.rides_id = rides.id
                            WHERE user_id = %s AND day_happened >= %s AND day_happened <= %s''', [user_id, start_date, end_date])
    receipts = []
    for r in rides:
        price = exec_get_one('''SELECT price FROM rides WHERE id = %s''', [r])
        numOfPassengers = exec_get_all('''SELECT id FROM passenger WHERE rides_id = %s''', [r])
        exec_commit('''UPDATE rides SET price = %s WHERE id = %s''', [(price[0]/len(numOfPassengers)), r])
        receipts += exec_get_one('''SELECT price FROM rides WHERE id = %s''', [r])
    return receipts

def getReview(driver, passenger):
    """Gets the review a rider has written"""
    return exec_get_one('''SELECT rating, review 
                            FROM reviews
                                INNER JOIN rides ON reviews.rides_id = rides.id
                                INNER JOIN passenger ON reviews.passenger_id = passenger.id
                            WHERE rides.driver = %s AND passenger.user_id = %s''', [driver, passenger])

def getResponse(driver, passenger):
    """Gets the response a driver has written to the review of the rider"""
    return exec_get_one('''SELECT response 
                            FROM reviews
                                INNER JOIN rides ON reviews.rides_id = rides.id
                                INNER JOIN passenger ON reviews.passenger_id = passenger.id
                            WHERE rides.driver = %s AND passenger.user_id = %s''', [driver, passenger])

def getAverageRating(ride_id):
    """Gets the average rating of a ride"""
    ratings = exec_get_all('''SELECT rating FROM reviews WHERE rides_id = %s''', [ride_id])
    if (ratings == []):
        return 0
    rating = 0.0
    count = 0
    for r in ratings:
        rating += r[0]
        count += 1
    return rating/count

def getFullRideInfo(start_date, end_date):
    """Gets aggregate rider information for all rides within 1 day of a given date"""
    rides = exec_get_all('''SELECT DISTINCT rides_id 
                            FROM passenger 
                                INNER JOIN rides ON passenger.rides_id = rides.id
                            WHERE day_happened >= %s AND day_happened <= %s''', [start_date, end_date])
    ride_info = []
    for r in rides:
        driver, id = exec_get_one('''SELECT name, rides.driver
                                    FROM rides
                                        INNER JOIN users ON users.id = rides.driver
                                    WHERE rides.id = %s''', [r])
        dest = exec_get_one('''SELECT destination FROM rides WHERE id = %s''', [r])
        riders = getRiders(id, dest)
        rating = getAverageRating(r)
        ride_info += [driver, dest, riders, rating]
    return ride_info

def getFareTimes():
    """Gets the average price for each hour"""
    hours = exec_get_all('''SELECT DISTINCT EXTRACT(HOUR FROM day_happened) FROM rides''')
    fares = []
    for h in hours:
        if (getAveragePrice(h[0]) != 0.0):
            fares += [h[0], getAveragePrice(h[0])]
    return fares