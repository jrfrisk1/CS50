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


# Admin login
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form["username"] and request.form["password"]:
            if (
                ADMIN_USER == request.form["username"]
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

        # try to set var from user input
        try:
            name = request.form["eventName"]
            host = request.form["hostedBy"]
            desc = request.form["description"]
            date = request.form["date"]
            start = request.form["startTime"]
            freq = request.form["frequency"]
        except:
            return redirect("/")

        date = datetime.strptime(date, "%Y-%m-%d").date()  # Format: YYYY-MM-DD
        start = datetime.strptime(start, "%H:%M").time()  # Format: HH:MM

        # Create a new entry into data base thats approved
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
            db_session.add(event)  # add event to session
            db_session.commit()
        except:
            db_session.rollback()

        return redirect("/admin-dash")

    # To show adamin dash
    else:
        if "username" in session:
            try:
                # Query approved events, ordered by event date
                events = (
                    db_session.query(Event)
                    .filter_by(status="Approved")
                    .order_by(Event.event_date.asc())
                    .all()
                )

                # Format start_time and event_date for display only, without altering the objects in the database
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
                db_session.rollback()  # Rollback session if any error occurs
                print(f"Error occurred: {e}")
                return redirect("/admin")  # Redirect on error

        return redirect("admin.html", error="Timed Out")


# Admin Dash delete-event
@app.route("/delete-event", methods=["POST"])
def deleteEvent():
    event_id = request.form.get("event_id")
    if id:
        event = db_session.query(Event).filter_by(id=event_id).first()

        if event:
            db_session.delete(event)
            db_session.commit()

    return redirect("/admin-dash")


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

    # Query approved events, ordered by event date
    events = (
        db_session.query(Event)
        .filter_by(status="Approved")
        .order_by(Event.event_date.asc())
        .all()
    )

    # Format start_time and event_date for display only, without altering the objects in the database
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
