from flask import Flask, flash, redirect, render_template, request, session # type: ignore
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash

# Create a Flask app instance
app = Flask(__name__)
app.secret_key = 'hello'  #TODO HIDE

# Ensure sessions is temp
app.config['SESSION_PERMANENT'] = False


# Store admin info
ADMIN_USER = 'admin' #TODO HIDE
ADMIN_PASS = '123' #TODO HIDE


# Admin login
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if ADMIN_PASS == password and username == ADMIN_USER:
            session['username'] = username
            return redirect ('/admin-dash')
        else:
            return render_template('admin.html', error='Invalid Login')
    return render_template('admin.html')


# Admin Dash
@app.route('/admin-dash', methods=['GET', 'POST'])
def admindash():
    if 'username' in session:
        return render_template('admindash.html')
    return render_template('admin.html', error='Timed Out')


# Submit Event
@app.route('/submit-event')
def submitevent():
    return render_template('submitevent.html')


# HomePage
@app.route('/')
def index():
    return render_template('index.html')


# Events
@app.route('/events')
def events():
    return render_template('events.html')


# Whats Kava
@app.route('/whats-kava')
def whatskava():
    return render_template('whatskava.html')


# Contact Us
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
