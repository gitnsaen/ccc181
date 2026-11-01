# sPrint: Campus Print Shop Queue Management System

**sPrint** is a queue management web application designed for university copy centers and student print kiosks. It eliminates front-counter congestion, USB drive bottlenecks, and unpredictable waiting times by enabling students to submit document print orders digitally, track their exact place in line in real time from anywhere on campus, and receive clear counter call notifications. Campus print shop operators manage incoming jobs efficiently using service-specific filters and rush priority handling.

## Setting
- **Setting:** University Student Center Copy & Print Shop
- **Problem Solved:** Long lines, lost files, and counter crowding during morning peak hours and assignment deadlines.

## Documentation
- [System Requirements Specification](docs/requirements.md): Living requirements document with functional and non-functional requirements, MVP scope, and user validation notes.
- [User Personas](docs/week3/personas.md): Target user profiles (Sammy Bautista and Kuya Jun Ramos) grounded in campus field research.

## Future Enhancements
- **Staff Authentication:** Staff routes are currently open for testing. Authentication and authorization will be added in Week 11 (see GitHub issue #8).

## How to Run
1. Copy the example environment file and set a local PostgreSQL password:
   ```bash
   cp .env.example .env
   ```
   Keep `.env` local; it is ignored by Git.
2. Start PostgreSQL and wait for it to become healthy:
   ```bash
   docker compose up -d
   docker compose ps
   ```
3. Activate the Python virtual environment:
   ```bash
   # On macOS / Linux:
   source .venv/bin/activate
   # On Windows:
   .venv\Scripts\activate
   ```
4. Install required packages (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```
5. Apply database migrations and load the starter services:
   ```bash
   flask --app app db upgrade
   flask --app app seed
   ```
6. Start the Flask application in debug mode:
   ```bash
   flask --app app run --debug
   ```
7. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

Use `docker compose down` to stop PostgreSQL while keeping its data volume.
