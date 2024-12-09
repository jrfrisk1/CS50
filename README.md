# Event Manager
#### Video Demo:  [<URL HERE>](https://youtu.be/suG7PhLlA1I)
#### Description:
# Flask Local Venue Events App

## Overview

This project is a web application built using Flask that allows users to view and manage events at a local venue. The app provides functionality to create, edit, and display events, ensuring a user-friendly experience. With PostgreSQL as the database backend, it efficiently handles event data, including details like frequency, iterations, and event-specific properties. The application is hosted on Heroku, making it accessible from anywhere.

The primary goal of this project was to design a scalable, intuitive, and functional app while tackling the challenges of managing recurring events and deploying a Flask app on Heroku. This README serves as a comprehensive guide to the project's structure, features, and design decisions.

---

## Features

1. **Event Management**:
   - Users can create events with properties such as:
     - Frequency (e.g., daily, weekly).
     - Number of iterations (e.g., repeat 10 times).
     - Event details (name, description, date, and time).
   - Events are stored in a PostgreSQL database.

2. **User-Friendly Display**:
   - Events are displayed in a clear, organized format on the homepage.
   - Upcoming events are highlighted.

3. **Responsive Design**:
   - The app is designed to work seamlessly across different devices.

4. **Deployment on Heroku**:
   - The app leverages Heroku Postgres for database management.
   - Fully integrated for live production use.

---

## Project Files

### 1. `app.py`
This is the main Flask application file that serves as the entry point for the project. Key functionalities include:
   - Routing for pages such as the homepage and event management.
   - Handling requests and responses for various endpoints.

### 2. `models.py`
This file contains the database models for the project, defining the structure of the event data and how it is stored in the PostgreSQL database.

### 3. `templates/`
Contains all the HTML templates used for the app's frontend:

### 4. `static/`
Includes static assets such as CSS files:
   - `styles.css`: Defines the app's styling for a polished look.

### 5. `requirements.txt`
Lists all Python dependencies required for the app, such as Flask, psycopg2, and others. Ensures smooth deployment on Heroku.

### 6. `Procfile`
A configuration file for Heroku specifying the command to run the application.

### 7. `README.md`
This file, documenting the project's purpose, structure, and usage.

---

## Design Decisions

### Event Properties
- **Why Frequency and Iterations?**
  Managing recurring events efficiently required breaking down event creation into frequency and iterations. This allows for flexibility in scheduling events while maintaining clarity.

### PostgreSQL
- **Why PostgreSQL?**
  PostgreSQL was chosen for its scalability and compatibility with Heroku. Its ability to handle complex queries makes it ideal for managing event data.

### Deployment
- **Why Heroku?**
  Heroku simplifies the deployment process while providing robust support for PostgreSQL. It enables rapid updates and live testing.

### Challenges
- **Database Schema Design:** Balancing simplicity with scalability when designing the event schema.
- **Deployment on Heroku:** Configuring environment variables and ensuring compatibility with Heroku’s Postgres setup.

---

## How to Use

1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```

2. Navigate to the project directory:
   ```bash
   cd flask-venue-events-app
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Create a PostgreSQL database.
   - Update the database URI as an environment variable.

5. Run the app locally:
   ```bash
   flask run
   ```

6. Access the app in your browser at `http://127.0.0.1:5000/`.

---

## Future Improvements

- Enable advanced filtering and sorting for events.
- Integrate a calendar view for better visualization.
- Optimize database queries for larger datasets.

---

## Conclusion

This Flask app demonstrates the ability to manage and display events effectively, leveraging the power of Flask, PostgreSQL, and Heroku. The design choices made throughout the project emphasize scalability, user-friendliness, and maintainability. This project serves as a robust foundation for further enhancements and features.

