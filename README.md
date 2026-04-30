# Purdue Rideshare

A web application that allows Purdue students to post, find, and request rides.
Built with Python (Flask) and MySQL for CS348: Information Systems.

## Features
- Register students and drivers
- Post, edit, and delete rides
- Request rides and accept/decline requests
- Filter and report on rides by date and destination

## Tech Stack
- **Backend:** Python, Flask
- **Database:** MySQL
- **Frontend:** HTML, Jinja2 templates

## Database Tables
- `Students` — stores student name, email, phone
- `Drivers` — links a student to their car info
- `Rides` — stores ride details posted by drivers
- `RideRequests` — stores ride requests made by students

## How to Run Locally

### Prerequisites
- Python 3
- MySQL running locally with a `purdue_rideshare` database

### Setup
1. Clone the repository
2. Install dependencies
3. In `app.py`, update `get_db()` with your MySQL credentials
4. Run the app: python app.py
5. Open your browser to `http://127.0.0.1:5000`

## Deployment
A live version of this app is deployed to Google Cloud Platform.
- **Live URL:** https://purdue-rideshare.uc.r.appspot.com (available through May 15, 2026)
- The GCP deployment code (modified `app.py`, `app.yaml`, `requirements.txt`) is on the `gcp-deployment` branch of this repository.
