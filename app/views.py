from datetime import datetime, timedelta
import random
import string
from bson import ObjectId
import pymongo
from app import app, conn
from flask import flash, jsonify, redirect, render_template, request, session, url_for


@app.route("/")
def index():
    from_airports = conn.airport_collection.find()
    to_airports = conn.airport_collection.find()
    today = datetime.now().date()
    return render_template("public/index.html",today=today, from_airports=from_airports, to_airports=to_airports)


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        return render_template("public/registration.html")
    else:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')

        values = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "password": password
        }
        conn.user_collection.insert_one(values)
        flash("Registered successully", "success")
        return redirect(request.url)


@app.route("/is-email-exist", methods=["GET"])
def is_email_exist():
    email = request.args.get("email")
    user = conn.user_collection.find_one({"email": email})
    if user == None:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("public/login.html", msg="")
    else:
        email = request.form.get("email")
        password = request.form.get("password")

        if password == 'admin' and email == 'admin@gmail.com':
            session['login'] = True
            session['role'] = "admin"
            return redirect("/admin")
        else:
            filter = {"email": email, "password": password}
            count = conn.user_collection.count_documents(filter)
            if count > 0:
                user = conn.user_collection.find_one(filter)
                session['login'] = True
                session['role'] = "customer"
                session['userName'] = user['first_name']+" "+user['last_name']
                session['user_id'] = str(user['_id'])
                return redirect("/")

    return render_template("public/login.html", msg="Invalid Login Credentials")


@app.route("/search")
def search():
    from_airports = conn.airport_collection.find()
    to_airports = conn.airport_collection.find()

    journey_type = request.args.get("journey_type")
    from_airport = ObjectId(request.args.get("from_airport"))
    to_airport = ObjectId(request.args.get("to_airport"))
    onward_date = request.args.get("onward_date")
    return_date = request.args.get("return_date")
    travel_class = request.args.get("travel_class")
    passengers = int(request.args.get("passengers"))

    if journey_type == "OneWay":
      filter = {
          "from_airport_id": from_airport,
          "to_airport_id": to_airport,
      }
      flights = conn.flight_collection.find(filter)
      source = conn.getAirportById(from_airport)
      destination = conn.getAirportById(to_airport)

      return render_template("public/search_oneway.html", from_airports=from_airports, to_airports=to_airports, flights=list(flights), journey_type=journey_type, from_airport=from_airport, to_airport=to_airport, onward_date=onward_date, return_date=return_date, travel_class=travel_class, passengers=passengers, source=source, destination=destination)
    else:
      oneward_filter = {
          "from_airport_id": ObjectId(from_airport),
          "to_airport_id": ObjectId(to_airport),
      }
      onward_flights = conn.flight_collection.find(oneward_filter)
      onward_source = conn.getAirportById(from_airport)
      onward_dest = conn.getAirportById(to_airport)

      return_filter = {
          "from_airport_id": ObjectId(to_airport),
          "to_airport_id": ObjectId(from_airport),
      }
      return_flights = conn.flight_collection.find(return_filter)
      return_source = conn.getAirportById(to_airport)
      return_dest = conn.getAirportById(from_airport)

    return render_template("public/search_round.html", from_airports=from_airports, to_airports=to_airports, onward_flights=list(onward_flights), return_flights=list(return_flights), journey_type=journey_type, from_airport=from_airport, to_airport=to_airport, onward_date=onward_date, return_date=return_date, travel_class=travel_class, passengers=passengers, onward_source=onward_source, onward_dest=onward_dest, return_source=return_source, return_dest=return_dest)


@app.route("/booking-confirmation", methods=["GET"])
def booking_confirmation():
    if not isLoggedIn():
      return redirect(url_for("login"))
    
    journey_type = request.args.get("journey_type")
    if journey_type == "OneWay":
      flight_id = ObjectId(request.args.get("flight_id"))
      source = request.args.get("source")
      destination = request.args.get("destination")
      onward_date = request.args.get("onward_date")
      onward_date = datetime.strptime(onward_date, "%Y-%m-%d")
      travel_class = request.args.get("travel_class")
      passengers = request.args.get("passengers")
      fare = request.args.get("fare")

      onward_flight = conn.flight_collection.find_one({'_id': flight_id})
      onward_source = conn.getAirportById(
      onward_flight['from_airport_id'])['airport_code']
      onward_dest = conn.getAirportById(onward_flight['to_airport_id'])['airport_code']
      onward_flight['departure_city_code'] = onward_source
      onward_flight['arrival_city_code'] = onward_dest

      return render_template("/public/booking-confirmation.html",round=round, onward_flight=onward_flight, journey_type=journey_type, source=source, destination=destination, onward_date=onward_date, travel_class=travel_class, passengers=int(passengers))
    else:
      onward_flight_id = ObjectId(request.args.get("onward_flight_id"))
      return_flight_id = ObjectId(request.args.get("return_flight_id"))
      onward_date = request.args.get("onward_date")
      onward_date = datetime.strptime(onward_date, "%Y-%m-%d")
      return_date = request.args.get("return_date")
      travel_class = request.args.get("travel_class")
      passengers = request.args.get("passengers")

      return render_template("/public/round-booking-confirmation.html",round=round)



@app.route("/booking-confirmation", methods=["POST"])
def booking_confirmation_post():
  journey_type = request.form.get('journey_type')
  onward_flight_id = ObjectId(request.form.get('onward_flight_id'))
  onward_departure_city_code = request.form.get('onward_departure_city_code')
  onward_arrival_city_code = request.form.get('onward_arrival_city_code')
  onward_departure_date = request.form.get('onward_departure_date')
  onward_departure_date = datetime.strptime(onward_departure_date, "%Y-%m-%d %H:%M:%S")
  onward_departure_time = request.form.get('onward_departure_time')
  onward_departure_time = datetime.strptime(onward_departure_time, "%Y-%m-%d %H:%M:%S")
  onward_arrival_time = request.form.get('onward_arrival_time')
  price = float(request.form.get('total_amount'))
  booked_on = datetime.now()
  passengers = request.form.get('passengers')
  passengers = int(passengers)

  terminal = random.randint(1,10)
  gate = random.choice(string.ascii_uppercase)  + str(random.randint(1,20))

  values = {    
    "user_id":ObjectId(session['user_id']),
    "journey_type":journey_type,
    "flight_id":onward_flight_id,
    "departure_city_code":onward_departure_city_code,
    "departure_date":onward_departure_date,
    "price":price,
    "booked_on":booked_on,
    "passengers":passengers,
    "status":"confirmed"
  }

  reservation = conn.reservation_collection.insert_one(values)
  reservation_id = ObjectId(reservation.inserted_id)

  #Insert Passengers
  for i in range(passengers):
    values = {
      "reservation_id":reservation_id,
      "first_name":request.form.get('first_name_'+str(i)),
      "last_name":request.form.get('last_name_'+str(i)),
      "email":request.form.get('email_'+str(i)),
      "phone_number":request.form.get('phone_number_'+str(i)),
      "state":request.form.get('state_'+str(i)),
      "zipcode":request.form.get('zipcode_'+str(i))
    }
    passenger = conn.passengers_collection.insert_one(values)
    passenger_id = ObjectId(passenger.inserted_id)

    old_seat_no = conn.boarding_collection.find_one({'flight_id': onward_flight_id,'departure_date':onward_departure_date},sort=[( '_id', pymongo.DESCENDING )])
    if old_seat_no != None:
      old_seat_no = int(old_seat_no['seat'])
      seat_no = old_seat_no+1
    else:
      seat_no = 1

    #insert boardingpass
    boarding_time = onward_departure_time - timedelta(hours=1)
    values ={
      "reservation_id":reservation_id,
      "passenger_id":passenger_id,
      "flight_id":onward_flight_id,
      "first_name":request.form.get('first_name_'+str(i)),
      "last_name":request.form.get('last_name_'+str(i)),
      "departure_city_code":onward_departure_city_code,
      "arrival_city_code":onward_arrival_city_code,
      "departure_date":onward_departure_date,
      "boarding_time":boarding_time,
      "terminal":terminal,
      "gate":gate,
      "seat":seat_no,      
    }
    conn.boarding_collection.insert_one(values)


  return redirect("/reservations")


@app.route("/reservations")
def view_reservations():
  user_id = ObjectId(session['user_id'])
  reservations = conn.reservation_collection.find({"user_id":user_id})
  reservations = list(reservations)
  list.reverse(reservations)
  return render_template("public/reservations.html", reservations=reservations, getFlightById=conn.getFlightById,getAirportById=conn.getAirportById)


@app.route("/cancel")
def cancel_reservation():
  reservation_id = ObjectId(request.args.get("reservation_id"))
  conn.reservation_collection.update_one({"_id":reservation_id},{'$set':{"status":"Cancelled"}})
  conn.boarding_collection.delete_many({"_id":reservation_id})
  return view_reservations()


@app.route("/passengers")
def view_passengers():
  reservation_id = ObjectId(request.args.get("reservation_id"))
  passengers = conn.passengers_collection.find({'reservation_id':reservation_id})
  return render_template("public/view-passengers.html",passengers=passengers)


@app.route("/borading-pass")
def view_boarding_pass():
  reservation_id = ObjectId(request.args.get("reservation_id"))
  passenger_id = ObjectId(request.args.get("passenger_id"))
  boarding = conn.boarding_collection.find_one({"reservation_id":reservation_id,"passenger_id":passenger_id})
  reservation = conn.reservation_collection.find_one({"_id":reservation_id})
  flight = conn.getFlightById(boarding["flight_id"])
  airline = conn.getAirlineById(flight["airline_id"])
  from_airport = conn.getAirportById(flight["from_airport_id"])
  to_airport = conn.getAirportById(flight["to_airport_id"])

  return render_template("/public/view-boardingpass.html",boarding=boarding, reservation=reservation, airline=airline, flight=flight, from_airport=from_airport, to_airport=to_airport)



@app.route("/logout")
def logout():
    session.clear()
    return index()


def isLoggedIn():
    if "login" not in session:
        return False
    else:
        return True
