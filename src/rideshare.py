from src.getRideshare import *
from src.updateRideshare import *
from src.swen344_db_utils import *
def rebuildTables():
    exec_sql_file("db-xlr7748/src/build.sql")

def fillTables():
    exec_sql_file("db-xlr7748/src/add_data.sql")

def createUser(name, instructions, rating, location, zipcode, date_joined, rider, available_rider, credit_card_num, driver, available_driver, car_make, car_model, license_num):
    """Adds a user into the users database"""
    exec_commit('''INSERT INTO users(name, instructions, rating, location, zipcode, date_joined, rider, available_rider, credit_card_num, driver, available_driver, car_make, car_model, license_num)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', [name, instructions, rating, location, zipcode, date_joined, rider, available_rider, credit_card_num, driver, available_driver, car_make, car_model, license_num])
    
def removeAccount(id):
    """Removes a user from the users database"""
    exec_commit('''DELETE FROM users WHERE id = %s''', [id])

def startRide(driver, passenger, price, starting_point, destination):
    """Starts a ride that other riders can join"""
    exec_commit('''INSERT INTO passenger(user_id)
                    VALUES (%s)''', [passenger])
    
    passenger_id = exec_get_one('''SELECT id FROM passenger WHERE user_id = %s''', [passenger])
    exec_commit('''INSERT INTO rides(driver, passenger_id, price, starting_point, destination)
                    VALUES (%s, %s, %s, %s, %s)''', [driver, passenger_id, price, starting_point, destination])
    
    joinRide(driver, passenger, destination)
    
def joinRide(driver, id, destination):
    """Adds a new rider to a current ride"""
    ride = exec_get_one('''SELECT id FROM rides WHERE driver = %s AND destination ~= %s''', [driver, destination])
    exec_commit('''INSERT INTO passenger(user_id, rides_id)
                    VALUES(%s, %s)''', [id, ride])

def writeReview(user_id, rides_id, rating, review):
    """Adds a review from a passenger about their ride"""
    passenger_id = exec_get_one('''SELECT id FROM passenger WHERE user_id = %s''', [user_id])
    exec_commit('''INSERT INTO reviews(passenger_id, rides_id, rating, review)
                    VALUES(%s, %s, %s, %s)''', [passenger_id, rides_id, rating, review])

def respondToReview(review_id, response):
    """Adds a response to the review from the driver of the ride"""
    exec_commit('''UPDATE reviews SET response = %s WHERE id = %s''', [response, review_id])

# def rideArranged(driver_id, passenger_id, driver_location, passenger_location):
#     updateLocation(driver_location, driver_id)
#     updateLocation(passenger_location, passenger_id)
#     return (exec_get_one('''SELECT location FROM users WHERE id = %s''', [driver_id]), 
#             exec_get_one('''SELECT location FROM users WHERE id = %s''', [passenger_id]))