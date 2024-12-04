from flask import Flask, flash, redirect, render_template, request, session, url_for
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Event, engine, init_db


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

''' Admin Routes'''

# Admin Login
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        # If username and password found
        if request.form["username"] and request.form["password"]:\
            # If username and password match
            if (
                ADMIN_USER == request.form["username"].lower()
                and ADMIN_PASS == request.form["password"]
            ):
                session["username"] = ADMIN_USER
                return redirect("/admin-dash")
            else:
                return render_template("admin/adminLogin.html", error="Invalid Login")
    if "username" in session:
        return redirect("/admin-dash")
    else:
        return render_template("admin/adminLogin.html")


# Admin Dash
@app.route("/admin-dash", methods=["GET", "POST"])
def admindash():
    if request.method == "POST":
        name = request.form.get("eventName")
        host = request.form.get("hostedBy")
        desc = request.form.get("description")
        date = request.form.get("date")
        start = request.form.get("startTime")
        freq = request.form.get("frequency")    
        img = request.files.get("imageUpload")    

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
        except Exception as e:
            db_session.rollback()
            flash(f"Event Failed To Create - {e}", "danger")

        return redirect("/admin-dash")

    else:
        # If logged in
        if "username" in session:
            try:
                today = datetime.today().date()

                approvedEvents = (
                    db_session.query(Event)
                    .filter(Event.status == "Approved", Event.event_date >= today)
                    .order_by(Event.event_date.asc())
                    .all()
                )
                
                pendingEvents = (
                    db_session.query(Event)
                    .filter(Event.status == "Pending", Event.event_date >= today)
                    .order_by(Event.event_date.asc())
                    .all()
                )
                pendingEventsFormatted = []
                
                approvedEventsFormatted = []
                for event in approvedEvents:
                    ApprovedFormattedEvent = {
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
                    approvedEventsFormatted.append(ApprovedFormattedEvent)
                
                for event in pendingEvents:
                    pendingFormattedEvent = {
                        "id": event.id,
                        "name": event.name,
                        "host": event.host,
                        "description": event.description[:350] + ". . .",
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
                    pendingEventsFormatted.append(pendingFormattedEvent)

                return render_template("/admin/adminDash.html", approvedEvents=approvedEventsFormatted,pendingEvents=pendingEventsFormatted)

            except Exception as e:
                db_session.rollback()
                flash(f"Error{e} ", "danger")
                return redirect("/admin")
        else:
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
            "host_link":event.host_link
        }
        formatted_events.append(formatted_event)
        return render_template("admin/editevent.html", formatted_event=formatted_event)
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
    host_link = request.form.get("hostLink")

    event_date_obj = (
        datetime.strptime(event_date, "%Y-%m-%d").date() if event_date else None
    )

    if start_time:
        try:
            start_time_obj = datetime.strptime(start_time, "%H:%M:%S").time()
        except ValueError:
            start_time_obj = datetime.strptime(start_time, "%H:%M").time()

    try:
        event = db_session.query(Event).filter_by(id=event_id).one_or_none()

        event.name = name
        event.host = host
        event.description = description
        event.event_date = event_date_obj
        event.start_time = start_time_obj
        event.frequency = frequency
        event.status = status
        event.host_link = host_link

        db_session.commit()
        flash("Event updated successfully.", "success")
        return redirect("/admin-dash")
    except Exception as e:
        flash(f"e", "danger")


# Admin Delete
@app.route("/delete-event", methods=["POST"])
def deleteEvent():
    event_id = request.form.get("event_id")
    if event_id:
        event = db_session.query(Event).filter_by(id=event_id).first()

        if event:
            db_session.delete(event)
            db_session.commit()
    else:
        flash("Cannot Find Event.", "danger")

    flash("Event Deleted.", "success")
    return redirect("/admin-dash")


@app.route("/approve-event", methods=["POST"])
def approveEvent():
    event_id = request.form.get("event_id")
    if event_id:
        event = db_session.query(Event).filter_by(id=event_id).first()
        
        event.status = "Approved"
        db_session.commit()
        flash("Event Approved", "success")
        return redirect("/admin-dash")


    flash("Event not found.", "success")
    return redirect("/admin-dash")

@app.route("/deny-event", methods=["POST"])
def denyEvent():
    event_id = request.form.get("event_id")
    if event_id:
        event = db_session.query(Event).filter_by(id=event_id).first()
        
        event.status = "Denied"
        db_session.commit()
        flash("Event Denied", "success")
        return redirect("/admin-dash")


    flash("Event not found.", "success")
    return redirect("/admin-dash")


'''Users Routes'''

# Submit Event
@app.route("/submit-event", methods=["POST","GET"])
def submitevent():
    if request.method == "POST":
        name = request.form.get("eventName")
        host = request.form.get("hostedBy")
        desc = request.form.get("description")
        date = request.form.get("date")
        start = request.form.get("startTime")
        freq = request.form.get("frequency")    
        link = request.form.get("hostLink")   

        date = datetime.strptime(date, "%Y-%m-%d").date()
        start = datetime.strptime(start, "%H:%M").time()

        event = Event(
            name=name,
            host=host,
            description=desc,
            event_date=date,
            start_time=start,
            frequency=freq,
            status="Pending",
            host_link=link
        )

        try:
            db_session.add(event)
            db_session.commit()
            flash("Event Submitted Successfully!", "success")
        except Exception as e:
            db_session.rollback()
            flash(f"Event Failed To Create - {e}", "danger")

        return redirect(request.referrer or "/")
    
# Events
@app.route("/")
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
            "description": event.description[:350] + ". . .",
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

    return render_template("/users/events.html", events=formatted_events)

@app.route("/event/<int:event_id>", methods=["POST","GET"])
def eventView(event_id):
    event = db_session.query(Event).filter_by(id=event_id).one_or_none()
    
    host_link = event.host_link
    
    if host_link and not (host_link.startswith("http://") or host_link.startswith("https://")):
        host_link = "https://" + host_link
    
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
        "host_link":host_link
    }

        
    
    return render_template('viewEvent.html',event=formatted_event,link=request.referrer or '/')

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
