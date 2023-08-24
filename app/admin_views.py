from datetime import datetime, timedelta
from app import app
from flask import flash, render_template, request, redirect, url_for
from app import conn
from bson import ObjectId
from app import APP_ROOT
from app.views import isLoggedIn


@app.route("/admin/")
def admin_index():
  if not isLoggedIn():
    return redirect(url_for("index"))

  return render_template("/admin/index.html")


@app.route("/admin/airlines", methods=["GET", "POST"])
def admin_airlines():
    if not isLoggedIn():
      return redirect(url_for("index"))
    
    if request.method == "POST":
        airline_name = request.form.get('airline_name')
        airline_id = request.form.get('airline_id')

        if airline_name != None:
            query = {"airline_name": airline_name}
            count = conn.airline_collection.count_documents(query)
            if count != 0:
                flash("This airline already exist", "warning")
                return redirect(request.url)

        if airline_id != "":
            conn.airline_collection.update_one({"_id": ObjectId(airline_id)}, {
                '$set': {"airline_name": airline_name}})
            flash("Airline updated successully", "success")
        else:
            conn.airline_collection.insert_one(
                {"airline_name": airline_name})
            flash("Airline added successully", "success")

        return redirect(request.url)
    else:
        airline_id = ObjectId(request.args.get("airline_id"))
        if airline_id != None:
            airline = conn.airline_collection.find_one({"_id": airline_id})

        airlines = conn.airline_collection.find()
        airlines = list(airlines)
        list.reverse(airlines)
        return render_template("admin/airlines.html", airlines=airlines, airline=airline)


@app.route("/admin/delete-airline")
def admin_delete_airline():
  airline_id = ObjectId(request.args.get("airline_id"))
  conn.airline_collection.delete_one({"_id":airline_id})
  flash("Airline deleted successully", "success")
  return admin_airlines()


@app.route("/admin/airplanes")
def admin_view_airplanes():
    if not isLoggedIn():
      return redirect(url_for("index"))

    airplanes = conn.airplane_collection.find()
    airplanes = list(airplanes)
    list.reverse(airplanes)
    return render_template("admin/airplanes.html", airplanes=airplanes, getAirlineById=conn.getAirlineById)


@app.route("/admin/add-airplane", methods=["GET", "POST"])
def admin_add_airplane():
    if not isLoggedIn():
      return redirect(url_for("index"))

    airlines = conn.airline_collection.find()

    if request.method == "POST":
      req = request.form
      airline_id = req.get("airline_id")
      airplane_type = req.get("airplane_type")
      airplane_capacity = req.get("airplane_capacity")

      query = {
        "airline_id":ObjectId(airline_id),
        "airplane_type":airplane_type,
        "airplane_capacity":int(airplane_capacity)
      }
      conn.airplane_collection.insert_one(query)
      flash("Airplane added successully", "success")
      return redirect(url_for("admin_view_airplanes"))
    else:
      return render_template("admin/airplane-save.html", airlines=airlines, airplane="")


@app.route("/admin/edit-airplane", methods=["GET", "POST"])
def admin_edit_airplane():
    if not isLoggedIn():
      return redirect(url_for("index"))

    airlines = conn.airline_collection.find()

    if request.method == "POST":
      req = request.form
      airplane_id = req.get("airplane_id")
      airline_id = req.get("airline_id")
      airplane_type = req.get("airplane_type")
      airplane_capacity = req.get("airplane_capacity")

      values = {
          "airline_id": ObjectId(airline_id),
          "airplane_type": airplane_type,
          "airplane_capacity": int(airplane_capacity)
      }
      conn.airplane_collection.update_one({"_id": ObjectId(airplane_id)}, {
                '$set': values})
      flash("Airplane updated successully", "success")
      return redirect(url_for("admin_view_airplanes"))
    else:
      airplane_id = ObjectId(request.args.get("airplane_id"))
      if airplane_id != None:
        airplane = conn.airplane_collection.find_one({"_id": airplane_id})

      return render_template("admin/airplane-save.html", airlines=airlines, airplane=airplane)


@app.route("/admin/delete-airplane")
def admin_delete_airplane():
  airplane_id = ObjectId(request.args.get("airplane_id"))
  conn.airplane_collection.delete_one({"_id":airplane_id})
  flash("Airplane deleted successully", "success")
  return admin_view_airplanes()


@app.route("/admin/airports")
def admin_view_airports():
    if not isLoggedIn():
      return redirect(url_for("index"))

    airports = conn.airport_collection.find()
    airports = list(airports)
    list.reverse(airports)
    return render_template("admin/airports.html", airports=airports)


@app.route("/admin/add-airport", methods=["GET", "POST"])
def admin_add_airport():
    if not isLoggedIn():
      return redirect(url_for("index"))

    if request.method == "POST":
      req = request.form
      airport_name = req.get("airport_name").lower().title()
      airport_code = req.get("airport_code").upper()
      airport_city = req.get("airport_city")
      airport_country = req.get("airport_country")

      query = {
        "airport_name":airport_name,
        "airport_code":airport_code,
        "airport_city":airport_city,
        "airport_country":airport_country,
      }
      conn.airport_collection.insert_one(query)
      flash("Airport added successully", "success")
      return redirect(url_for("admin_view_airports"))
    else:
      return render_template("admin/airport-save.html",airport="")


@app.route("/admin/edit-airport", methods=["GET", "POST"])
def admin_edit_airport():
    if not isLoggedIn():
      return redirect(url_for("index"))

    if request.method == "POST":
      req = request.form
      airport_id = req.get("airport_id")
      airport_name = req.get("airport_name").lower().title()
      airport_code = req.get("airport_code").upper()
      airport_city = req.get("airport_city")
      airport_country = req.get("airport_country")

      values = {
        "airport_name":airport_name,
        "airport_code":airport_code,
        "airport_city":airport_city,
        "airport_country":airport_country,
      }
      conn.airport_collection.update_one({"_id": ObjectId(airport_id)}, {
                '$set': values})
      flash("Airport updated successully", "success")
      return redirect(url_for("admin_view_airports"))
    else:
      airport_id = ObjectId(request.args.get("airport_id"))
      if airport_id != None:
        airport = conn.airport_collection.find_one({"_id": airport_id})

      return render_template("admin/airport-save.html",airport=airport)


@app.route("/admin/delete-airport")
def admin_delete_airport():
  airport_id = ObjectId(request.args.get("airport_id"))
  conn.airport_collection.delete_one({"_id":airport_id})
  flash("Airplane deleted successully", "success")
  return admin_view_airplanes()


@app.route("/admin/flights")
def admin_view_flights():
    if not isLoggedIn():
      return redirect(url_for("index"))

    flights = conn.flight_collection.find()
    flights = list(flights)
    list.reverse(flights)
    return render_template("admin/flights.html",getAirplaneById3=getAirplaneById3, flights=flights, getAirlineById=conn.getAirlineById,getAirportById=conn.getAirportById)


@app.route("/admin/add-flight", methods=["GET", "POST"])
def admin_add_flight():
    if not isLoggedIn():
      return redirect(url_for("index"))

    airlines = conn.airline_collection.find()
    from_airports = conn.airport_collection.find()
    to_airports = conn.airport_collection.find()
    airplanes = conn.airplane_collection.find()
    if request.method == "POST":
      req = request.form
      flight_no = req.get("flight_no")
      airline_id = req.get("airline_id")
      from_airport_id = req.get("from_airport_id")
      to_airport_id = req.get("to_airport_id")
      departure_time = req.get("departure_time")
      arrival_time = req.get("arrival_time")
      available_seats = req.get("available_seats")
      fare = req.get("fare")
      arrival_time3 = arrival_time
      departure_time3 = departure_time
      departure_time = datetime.strptime(departure_time,"%H:%M")
      arrival_time = datetime.strptime(arrival_time,"%H:%M")
      if departure_time < arrival_time :
          difference = arrival_time - departure_time
      else:
          arrival_time2 = datetime.now() + timedelta(1)
          arrival_time2 = str(arrival_time2.date())+" "+arrival_time3
          arrival_time = datetime.strptime(arrival_time2, "%Y-%m-%d %H:%M")

          departure_time2 = datetime.now()
          departure_time2 = str(departure_time2.date()) + " " + departure_time3
          departure_time = datetime.strptime(departure_time2, "%Y-%m-%d %H:%M")

          difference = arrival_time - departure_time
          print(arrival_time)
          print(departure_time)
          print(difference)

      total_seconds = difference.total_seconds()
      min, sec = divmod(total_seconds, 60)
      hrs, min = divmod(min, 60)
      duration = "%d hrs %02d min" % (hrs, min)
      airplane = conn.airplane_collection.find_one({"_id": ObjectId(airline_id)})
      query = {
        "flight_no":flight_no,
        "airplane_id":ObjectId(airline_id),
        "airline_id": airplane['airline_id'],
        "from_airport_id":ObjectId(from_airport_id),
        "to_airport_id":ObjectId(to_airport_id),
        "departure_time":departure_time,
        "arrival_time":arrival_time,
        "duration":duration,
        "available_seats":available_seats,
        "fare":float(fare),
      }
      conn.flight_collection.insert_one(query)
      flash("Flight added successully", "success")
      return redirect(url_for("admin_view_flights"))
    else:
      return render_template("admin/flight-save.html",getAirlineById2=getAirlineById2,airplanes=airplanes,airlines=airlines,from_airports=from_airports,to_airports=to_airports,getAirlineById=conn.getAirlineById,getAirportById=conn.getAirportById,flight="")

def getAirlineById2(airline_id):
    airline = conn.airline_collection.find_one({"_id":airline_id})
    return airline

def getAirplaneById3(airplane_id):
    airplane = conn.airplane_collection.find_one({"_id":airplane_id})
    return airplane
@app.route("/admin/edit-flight", methods=["GET", "POST"])
def admin_edit_flight():
    if not isLoggedIn():
      return redirect(url_for("index"))
      
    airlines = conn.airline_collection.find()
    from_airports = conn.airport_collection.find()
    to_airports = conn.airport_collection.find()

    if request.method == "POST":
      req = request.form
      flight_id = req.get("flight_id")
      flight_no = req.get("flight_no")
      airline_id = req.get("airline_id")
      from_airport_id = req.get("from_airport_id")
      to_airport_id = req.get("to_airport_id")
      departure_time = req.get("departure_time")
      arrival_time = req.get("arrival_time")
      available_seats = req.get("available_seats")
      fare = req.get("fare")
      
      departure_time = datetime.strptime(departure_time,"%H:%M")
      arrival_time = datetime.strptime(arrival_time,"%H:%M")
     
      difference = arrival_time - departure_time

      total_seconds = difference.total_seconds()
      min, sec = divmod(total_seconds, 60)
      hrs, min = divmod(min, 60)
      duration = "%d hrs %02d min" % (hrs, min)     

      values = {
        "flight_no":flight_no,
        "airline_id":ObjectId(airline_id),
        "from_airport_id":ObjectId(from_airport_id),
        "to_airport_id":ObjectId(to_airport_id),
        "departure_time":departure_time,
        "arrival_time":arrival_time,
        "duration":duration,
        "available_seats":int(available_seats),
        "fare":float(fare)
      }
      conn.flight_collection.update_one({"_id": ObjectId(flight_id)}, {
                '$set': values})
      flash("Flight updated successully", "success")
      return redirect(url_for("admin_view_flights"))
    else:
      flight_id = ObjectId(request.args.get("flight_id"))
      if flight_id != None:
        flight = conn.flight_collection.find_one({"_id": flight_id})

      return render_template("admin/flight-save.html",airlines=airlines,from_airports=from_airports,to_airports=to_airports,getAirlineById=conn.getAirlineById,getAirportById=conn.getAirportById,flight=flight)


@app.route("/admin/delete-flight")
def admin_delete_flight():
  flight_id = ObjectId(request.args.get("flight_id"))
  conn.flight_collection.delete_one({"_id":flight_id})
  flash("Flight deleted successully", "success")
  return admin_view_airplanes()


@app.route("/admin/reservations")
def admin_view_reservations():
  reservations = conn.reservation_collection.find()
  reservations = list(reservations)
  list.reverse(reservations)
  return render_template("admin/reservations.html", reservations=reservations, getFlightById=conn.getFlightById,getAirportById=conn.getAirportById)


@app.route("/admin/passengers")
def admin_view_passengers():
  reservation_id = ObjectId(request.args.get("reservation_id"))
  passengers = conn.passengers_collection.find({'reservation_id':reservation_id})
  return render_template("admin/passengers.html",passengers=passengers)


@app.route("/admin/borading-pass")
def admin_view_boarding_pass():
  reservation_id = ObjectId(request.args.get("reservation_id"))
  passenger_id = ObjectId(request.args.get("passenger_id"))
  boarding = conn.boarding_collection.find_one({"reservation_id":reservation_id,"passenger_id":passenger_id})
  reservation = conn.reservation_collection.find_one({"_id":reservation_id})
  flight = conn.getFlightById(boarding["flight_id"])
  airline = conn.getAirlineById(flight["airline_id"])
  from_airport = conn.getAirportById(flight["from_airport_id"])
  to_airport = conn.getAirportById(flight["to_airport_id"])

  return render_template("/admin/boardingpass.html",boarding=boarding, reservation=reservation, airline=airline, flight=flight, from_airport=from_airport, to_airport=to_airport)


@app.route("/admin/cancel")
def admin_cancel_reservation():
  reservation_id = ObjectId(request.args.get("reservation_id"))
  conn.reservation_collection.update_one({"_id":reservation_id},{'$set':{"status":"Cancelled"}})
  conn.boarding_collection.delete_many({"_id":reservation_id})
  return admin_view_reservations()

  

