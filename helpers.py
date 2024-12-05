from datetime import datetime, timedelta
from models import Event

def createEvent(feq):
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
