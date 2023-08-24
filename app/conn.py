from bson import ObjectId
import pymongo

dbClient = pymongo.MongoClient('mongodb://localhost:27017/')
db = dbClient["airline"]

airline_collection = db['Airlines']
airplane_collection = db['Airplanes']
airport_collection = db['Airports']
flight_collection = db['Flights']
user_collection = db['Users']
reservation_collection = db['Reservations']
passengers_collection = db['Passengers']
boarding_collection = db['BoardingPass']


def getAirlineById(airlineId):
    query = {"_id": ObjectId(airlineId)}
    return  airline_collection.find_one(query)    


def getAirplaneById(airplaneId):
    query = {"_id": ObjectId(airplaneId)}
    return airplane_collection.find_one(query)


def getAirportById(airportId):
    query = {"_id": ObjectId(airportId)}
    return airport_collection.find_one(query)


def getFlightById(flightId):
    query = {"_id": ObjectId(flightId)}
    return flight_collection.find_one(query)


def getUserById(userId):
    query = {"_id": ObjectId(userId)}
    return user_collection.find_one(query)



    
