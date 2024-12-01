from flask import Flask, flash, redirect, render_template, request, session  # type: ignore
from datetime import datetime
from sqlalchemy.orm import sessionmaker

from models import Event, engine, init_db
from helpers import convert_to_ampm, dbToUserDate

# Create a Flask app instance
app = Flask(__name__)
app.secret_key = "hello"  # TODO HIDE

# Initialize the database (create tables if they don't exist)
Session = sessionmaker(bind=engine)
db_session = Session()

# Create a session instance
init_db()

# Ensure sessions is temp
app.config["SESSION_PERMANENT"] = False

# Store admin info
ADMIN_USER = "admin"  # TODO HIDE
ADMIN_PASS = "123"  # TODO HIDE

# Admin Routes


# Admin Login
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form["username"] and request.form["password"]:
            if (
                ADMIN_USER == request.form["username"].lower()
                and ADMIN_PASS == request.form["password"]
            ):
                session["username"] = ADMIN_USER
                return redirect("/admin-dash")
            else:
                return render_template("admin.html", error="Invalid Login")

    return render_template("admin.html")


# Admin Dash
@app.route("/admin-dash", methods=["GET", "POST"])
def admindash():
    if request.method == "POST":
        try:
            name = request.form["eventName"]
            host = request.form["hostedBy"]
            desc = request.form["description"]
            date = request.form["date"]
            start = request.form["startTime"]
            freq = request.form["frequency"]
        except:
            return redirect("/")

        date = datetime.strptime(date, "%Y-%m-%d").date()
        start = datetime.strptime(start, "%H:%M").time()

        event = Event(
            name=name,
            host=host,
            description=desc,
            event_date=date,
            start_time=start,
            frequency=freq,
            status="Approved",
        )

        try:
            db_session.add(event)
            db_session.commit()
            flash("Event Created Successfully!", "success")
        except:
            db_session.rollback()
            flash("Event Failed To Create", "danger")

        return redirect("/admin-dash")

    else:
        if "username" in session:
            try:
                today = datetime.today().date()

                events = (
                    db_session.query(Event)
                    .filter(Event.status == "Approved", Event.event_date >= today)
                    .order_by(Event.event_date.asc())
                    .all()
                )

                formatted_events = []
                for event in events:
                    formatted_event = {
                        "id": event.id,
                        "name": event.name,
                        "host": event.host,
                        "description": event.description,
                        "event_date": (
                            event.event_date.strftime("%m/%d/%Y")
                            if event.event_date
                            else None
                        ),
                        "start_time": (
                            event.start_time.strftime("%I:%M %p")
                            if event.start_time
                            else None
                        ),
                        "frequency": event.frequency,
                        "status": event.status,
                        "created_at": event.created_at,
                        "updated_at": event.updated_at,
                    }
                    formatted_events.append(formatted_event)

                return render_template("admindash.html", events=formatted_events)

            except Exception as e:
                db_session.rollback()
                flash("Error", "danger")
                return redirect("/admin")

        flash("Not Logged In.", "danger")
        return redirect("/admin")


# Admin Edit
@app.route("/edit-event", methods=["GET", "POST"])
def editEvent():

    event_id = request.form.get("event_id")
    if event_id:
        formatted_events = []
        event = db_session.query(Event).filter_by(id=event_id).first()

        formatted_event = {
            "id": event.id,
            "name": event.name,
            "host": event.host,
            "description": event.description,
            "event_date": event.event_date,
            "start_time": event.start_time,
            "frequency": event.frequency,
            "status": event.status,
            "created_at": event.created_at,
            "updated_at": event.updated_at,
        }
        formatted_events.append(formatted_event)
        return render_template("editevent.html", formatted_event=formatted_event)
    else:
        flash("Event Not Found", "danger")


# Admin Update
@app.route("/update_event/<int:event_id>", methods=["POST"])
def updateEvent(event_id):
    name = request.form.get("name")
    host = request.form.get("host")
    description = request.form.get("description")
    event_date = request.form.get("event_date")
    start_time = request.form.get("start_time")
    frequency = request.form.get("frequency")
    status = request.form.get("status")

    event_date_obj = (
        datetime.strptime(event_date, "%Y-%m-%d").date() if event_date else None
    )

    if start_time:
        try:
            start_time_obj = datetime.strptime(start_time, "%H:%M:%S").time()
        except ValueError:
            start_time_obj = datetime.strptime(start_time, "%H:%M").time()

    event = db_session.query(Event).filter_by(id=event_id).one_or_none()

    event.name = name
    event.host = host
    event.description = description
    event.event_date = event_date_obj
    event.start_time = start_time_obj
    event.frequency = frequency
    event.status = status

    db_session.commit()
    flash("Event updated successfully.", "success")
    return redirect("/admin-dash")


# Admin Delete
@app.route("/delete-event", methods=["POST"])
def deleteEvent():
    event_id = request.form.get("event_id")
    if id:
        event = db_session.query(Event).filter_by(id=event_id).first()

        if event:
            db_session.delete(event)
            db_session.commit()
    else:
        flash("Cannot Find Event.", "danger")

    flash("Event Deleted.", "success")
    return redirect("/admin-dash")


# Users Routes


# Submit Event
@app.route("/submit-event")
def submitevent():
    return render_template("submitevent.html")


# HomePage
@app.route("/")
def index():
    return render_template("index.html")


# Events
@app.route("/events")
def events():

    today = datetime.today().date()

    # Query approved events, ordered by event date
    events = (
        db_session.query(Event)
        .filter(Event.status == "Approved", Event.event_date >= today)
        .order_by(Event.event_date.asc())
        .all()
    )

    formatted_events = []
    for event in events:
        formatted_event = {
            "id": event.id,
            "name": event.name,
            "host": event.host,
            "description": event.description,
            "event_date": (
                event.event_date.strftime("%m/%d/%Y") if event.event_date else None
            ),
            "start_time": (
                event.start_time.strftime("%I:%M %p") if event.start_time else None
            ),
            "frequency": event.frequency,
            "status": event.status,
            "created_at": event.created_at,
            "updated_at": event.updated_at,
        }
        formatted_events.append(formatted_event)

    return render_template("events.html", events=formatted_events)


# Whats Kava
@app.route("/whats-kava")
def whatskava():
    return render_template("whatskava.html")


# Contact Us
@app.route("/contact")
def contact():
    return render_template("contact.html")


# Run the application
if __name__ == "__main__":
    app.run(debug=True)
