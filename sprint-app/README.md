# sPrint: Campus Print Shop Queue Management System

**sPrint** is a queue management web application designed for university copy centers and student print kiosks. It eliminates front-counter congestion, USB drive bottlenecks, and unpredictable waiting times by enabling students to submit document print orders digitally, track their exact place in line in real time from anywhere on campus, and receive clear counter call notifications. Campus print shop operators manage incoming jobs efficiently using service-specific filters and rush priority handling.

## Setting
- **Setting:** University Student Center Copy & Print Shop
- **Problem Solved:** Long lines, lost files, and counter crowding during morning peak hours and assignment deadlines.

## How to Run
1. Activate the Python virtual environment:
   ```bash
   # On macOS / Linux:
   source .venv/bin/activate
   # On Windows:
   .venv\Scripts\activate
   ```
2. Install required packages (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```
3. Start the Flask application in debug mode:
   ```bash
   flask --app app run --debug
   ```
4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```
