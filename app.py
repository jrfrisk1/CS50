from flask import Flask, flash, redirect, render_template, request, session, url_for,g
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from models import Event, engine, init_db,Counter
from dateutil.relativedelta import relativedelta
import os




# Create a Flask app instance
app = Flask(__name__)
app.secret_key = "hello"  
app.config['DEBUG'] = True 
# Initialize the database (create tables if they don't exist)
Session = sessionmaker(bind=engine)
db_session = Session()

# Create a session instance
init_db()

# Ensure sessions is temp
app.config["SESSION_PERMANENT"] = False

# Store admin info
ADMIN_USER = "admin"  
ADMIN_PASS = "123"  




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
    return render_template("admin/adminLogin.html")


# Admin Dash
@app.route("/admin-dash", methods=["GET"])
def admindash():
        # If logged in
    if request.method == 'GET':
        if "username" in session:
            try:
                today = datetime.today().date()

                approvedEvents = (
                    db_session.query(Event)
                    .filter(Event.status == "Approved", Event.event_date >= today)
                    .order_by(Event.event_date.asc())
                    .limit(10)
                    .all()
                )
                
                pendingEvents = (
                    db_session.query(Event)
                    .filter(Event.status == "Pending", Event.event_date >= today)
                    .distinct(Event.eventId)
                    .order_by(Event.eventId, Event.event_date.asc())
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
                        "eventId": event.eventId
                    }
                    approvedEventsFormatted.append(ApprovedFormattedEvent)
                
                for event in pendingEvents:
                    pendingFormattedEvent = {
                        "id": event.id,
                        "name": event.name,
                        "host": event.host,
                        "description": f"{event.description[:350]} . . ." if len(event.description) > 350 else event.description,
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
                        "eventId": event.eventId
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
        events = db_session.query(Event).filter_by(eventId=event_id).all()
        for event in events:
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
                "host_link":event.host_link,
                "eventId": event.eventId
            }
            formatted_events.append(formatted_event)
        return render_template("admin/editevent.html", formatted_event=formatted_event)
    else:
        flash("Event Not Found", "danger")


# Admin Update
@app.route("/update_event/<int:eventId>", methods=["POST"])
def updateEvent(eventId):
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
        events = db_session.query(Event).filter_by(eventId=eventId).all()

        for event in events:
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
    today = datetime.today().date()
    event_id = request.form.get("event_id")
    if event_id:
        events = db_session.query(Event).filter_by(eventId=event_id).all()
        for event in events:
            db_session.delete(event)
        oldEvents = db_session.query(Event).filter(Event.event_date < today).all()
        for old in oldEvents:
            db_session.delete(old)
    
    db_session.commit()
           

    flash("Event Deleted.", "success")
    return redirect("/admin-dash")


@app.route("/approve-event", methods=["POST"])
def approveEvent():
    event_id = request.form.get("event_id")
    if event_id:
        try:
            db_session.query(Event).filter_by(eventId=event_id).update({"status": "Approved"})
            db_session.commit()
            flash("Events Approved Successfully!", "success")
        except Exception as e:
            db_session.rollback()
            flash(f"Failed to approve events: {e}", "danger")
        return redirect("/admin-dash")


    flash("Event not found.", "success")
    return redirect("/admin-dash")

@app.route("/deny-event", methods=["POST"])
def denyEvent():
    event_id = request.form.get("event_id")
    print(f"Received event_id: {event_id}")
    if event_id:
        events = db_session.query(Event).filter_by(eventId=int(event_id)).all()
        for event in events:
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
    

    counter = db_session.query(Counter).one_or_none()
    if not counter:
        main = Counter(count=0)
        db_session.add(main)
        db_session.commit()
        counter = db_session.query(Counter).one_or_none()
    else:    
        counter.count += 1
        db_session.commit()      
            
    if request.method == "POST":
        eventDict = {
        'name' : request.form.get("eventName"),
        'host' : request.form.get("hostedBy"),
        'desc' : request.form.get("description"),
        'date' : request.form.get("date"),
        'start' : request.form.get("startTime"),
        'freq' : request.form.get("frequency"),    
        'link' : request.form.get("hostLink"),  }

        date = datetime.strptime(eventDict['date'], "%Y-%m-%d").date()
        start = datetime.strptime(eventDict['start'], "%H:%M").time()
        
        def createEvent(freq, iterations, eventDict, ):
            eventsList=[]
            for n in range(iterations):
                if freq:
                    event_date = date + (n * freq)
                else:
                    event_date = date

                event = Event(
                    name=eventDict['name'],
                    host=eventDict['host'],
                    description=eventDict['desc'],
                    event_date=event_date,
                    start_time=start,
                    frequency=eventDict['freq'],
                    status="Pending",
                    host_link=eventDict['link'],
                    eventId =  counter.count
                )
                eventsList.append(event)
            try:
                db_session.bulk_save_objects(eventsList)
                db_session.commit()
                flash("Event saved Successfully!", "success")
                
            except Exception as e:
                db_session.rollback()
                flash(f"Event Failed To SAVE - {e}", "danger")

        try:
            match eventDict['freq']:
                case "yearly":
                    createEvent(timedelta(days=365),5, eventDict)
                case "monthly":
                    createEvent(relativedelta(months=1),(5*12), eventDict)
                case "weekly":
                    createEvent(timedelta(weeks=1),(5*52), eventDict)
                case "oneTime":
                    createEvent(None, 1, eventDict)
            flash("Event Submitted Successfully!", "success")
        except Exception as e:
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
            "description": f"{event.description[:350]} . . ." if len(event.description) > 350 else event.description,
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
