from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ.get("DB_PASSWORD", "password123"),
        database="purdue_rideshare"
    )

# Home page - list all rides
@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.ride_id, r.destination, r.meetup_location, r.departure_date,
               r.departure_time, r.seats_available, r.description,
               r.request_count, r.accepted_count,
               s.name as driver_name
        FROM Rides r
        JOIN Drivers d ON r.driver_id = d.driver_id
        JOIN Students s ON d.student_id = s.student_id
        ORDER BY r.departure_date, r.departure_time
    """)
    rides = cursor.fetchall()
    cursor.execute("SELECT student_id, name FROM Students ORDER BY name")
    students = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("index.html", rides=rides, students=students)

# Add ride page
@app.route("/rides/add", methods=["GET", "POST"])
def add_ride():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == "POST":
        cursor.execute("""
            INSERT INTO Rides (driver_id, meetup_location, destination,
                departure_date, departure_time, seats_available, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            request.form["driver_id"],
            request.form["meetup_location"],
            request.form["destination"],
            request.form["departure_date"],
            request.form["departure_time"],
            request.form["seats_available"],
            request.form["description"]
        ))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for("index"))
    cursor.execute("""
        SELECT d.driver_id, s.name, d.car_model, d.car_color
        FROM Drivers d JOIN Students s ON d.student_id = s.student_id
    """)
    drivers = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("add_ride.html", drivers=drivers)

# Edit ride page
@app.route("/rides/edit/<int:ride_id>", methods=["GET", "POST"])
def edit_ride(ride_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == "POST":
        cursor.execute("""
            UPDATE Rides SET driver_id=%s, meetup_location=%s, destination=%s,
                departure_date=%s, departure_time=%s, seats_available=%s, description=%s
            WHERE ride_id=%s
        """, (
            request.form["driver_id"],
            request.form["meetup_location"],
            request.form["destination"],
            request.form["departure_date"],
            request.form["departure_time"],
            request.form["seats_available"],
            request.form["description"],
            ride_id
        ))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for("index"))
    cursor.execute("SELECT * FROM Rides WHERE ride_id = %s", (ride_id,))
    ride = cursor.fetchone()
    cursor.execute("""
        SELECT d.driver_id, s.name, d.car_model, d.car_color
        FROM Drivers d JOIN Students s ON d.student_id = s.student_id
    """)
    drivers = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("edit_ride.html", ride=ride, drivers=drivers)

# Delete ride
@app.route("/rides/delete/<int:ride_id>", methods=["POST"])
def delete_ride(ride_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM RideRequests WHERE ride_id = %s", (ride_id,))
    cursor.execute("DELETE FROM Rides WHERE ride_id = %s", (ride_id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for("index"))

# Report page
@app.route("/report")
def report():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")
    destination = request.args.get("destination", "")
    query = """
        SELECT r.ride_id, r.destination, r.meetup_location, r.departure_date,
               r.departure_time, r.seats_available, r.description,
               r.request_count, r.accepted_count,
               s.name as driver_name
        FROM Rides r
        JOIN Drivers d ON r.driver_id = d.driver_id
        JOIN Students s ON d.student_id = s.student_id
        WHERE 1=1
    """
    params = []
    if start_date:
        query += " AND r.departure_date >= %s"
        params.append(start_date)
    if end_date:
        query += " AND r.departure_date <= %s"
        params.append(end_date)
    if destination:
        query += " AND r.destination LIKE %s"
        params.append(f"%{destination}%")
    query += " ORDER BY r.departure_date, r.departure_time"
    cursor.execute(query, params)
    rides = cursor.fetchall()
    stats = None
    if rides:
        total_rides = len(rides)
        avg_seats = sum(r["seats_available"] for r in rides) / total_rides
        avg_requests = sum(r["request_count"] for r in rides) / total_rides
        avg_accepted = sum(r["accepted_count"] for r in rides) / total_rides
        total_requests = sum(r["request_count"] for r in rides)
        total_accepted = sum(r["accepted_count"] for r in rides)
        acceptance_rate = (total_accepted / total_requests * 100) if total_requests > 0 else 0
        stats = {
            "total_rides": total_rides,
            "avg_seats": round(avg_seats, 1),
            "avg_requests": round(avg_requests, 1),
            "avg_accepted": round(avg_accepted, 1),
            "acceptance_rate": round(acceptance_rate, 1)
        }
    cursor.execute("SELECT DISTINCT destination FROM Rides ORDER BY destination")
    destinations = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("report.html", rides=rides, stats=stats,
                           destinations=destinations, start_date=start_date,
                           end_date=end_date, destination=destination)

# Add student
@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == "POST":
        cursor.execute("""
            INSERT INTO Students (name, email, phone) VALUES (%s, %s, %s)
        """, (request.form["name"], request.form["email"], request.form["phone"]))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for("index"))
    cursor.close()
    db.close()
    return render_template("add_student.html")

# Add driver
@app.route("/drivers/add", methods=["GET", "POST"])
def add_driver():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == "POST":
        cursor.execute("""
            INSERT INTO Drivers (student_id, car_model, license_plate, car_color)
            VALUES (%s, %s, %s, %s)
        """, (request.form["student_id"], request.form["car_model"],
              request.form["license_plate"], request.form["car_color"]))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for("index"))
    cursor.execute("""
        SELECT s.student_id, s.name FROM Students s
        WHERE s.student_id NOT IN (SELECT student_id FROM Drivers)
    """)
    students = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("add_driver.html", students=students)

# Request a ride
@app.route("/rides/request/<int:ride_id>", methods=["POST"])
def request_ride(ride_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        # REPEATABLE READ prevents phantom reads if two students
        # request the same ride simultaneously
        cursor.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")
        cursor.execute("START TRANSACTION")

        student_id = request.form["student_id"]
        cursor.execute("""
            SELECT * FROM RideRequests WHERE ride_id=%s AND student_id=%s FOR UPDATE
        """, (ride_id, student_id))
        existing = cursor.fetchone()

        if not existing:
            cursor.execute("""
                INSERT INTO RideRequests (ride_id, student_id, status) VALUES (%s, %s, 'pending')
            """, (ride_id, student_id))
            cursor.execute("""
                UPDATE Rides SET request_count = request_count + 1 WHERE ride_id = %s
            """, (ride_id,))

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Transaction error: {e}")
    finally:
        cursor.close()
        db.close()
    return redirect(url_for("index"))

# View requests for a ride (driver's view)
@app.route("/rides/<int:ride_id>/requests")
def view_requests(ride_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT rr.request_id, rr.status, s.name, s.email, s.phone
        FROM RideRequests rr
        JOIN Students s ON rr.student_id = s.student_id
        WHERE rr.ride_id = %s
    """, (ride_id,))
    requests_list = cursor.fetchall()
    cursor.execute("""
        SELECT r.*, s.name as driver_name FROM Rides r
        JOIN Drivers d ON r.driver_id = d.driver_id
        JOIN Students s ON d.student_id = s.student_id
        WHERE r.ride_id = %s
    """, (ride_id,))
    ride = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template("view_requests.html", requests=requests_list, ride=ride)

# Accept or decline a request
@app.route("/requests/<int:request_id>/<action>", methods=["POST"])
def update_request(request_id, action):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        # SERIALIZABLE prevents two drivers from accepting the same
        # request concurrently, ensuring accepted_count stays accurate
        cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
        cursor.execute("START TRANSACTION")

        status = "accepted" if action == "accept" else "declined"
        cursor.execute("""
            SELECT ride_id FROM RideRequests WHERE request_id = %s FOR UPDATE
        """, (request_id,))
        row = cursor.fetchone()
        ride_id = row["ride_id"]

        cursor.execute("""
            UPDATE RideRequests SET status = %s WHERE request_id = %s
        """, (status, request_id))

        if status == "accepted":
            cursor.execute("""
                UPDATE Rides SET accepted_count = accepted_count + 1 WHERE ride_id = %s
            """, (ride_id,))

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Transaction error: {e}")
    finally:
        cursor.close()
        db.close()
    return redirect(url_for("view_requests", ride_id=ride_id))

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)