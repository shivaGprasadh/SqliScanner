# SQLi Scanner Application Documentation

## Overview

This repository contains a SQL injection vulnerability scanner web application built with Flask. The application provides a user-friendly interface for running SQLMap scans against websites to detect potential SQL injection vulnerabilities. Users can configure various scanning options, view scan progress in real-time, and review detailed results of completed scans.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The SQLi Scanner is built as a Flask web application with a SQLAlchemy ORM database layer, providing an intuitive UI for SQLMap, which is a powerful command-line SQL injection detection tool.

### Key Architectural Decisions

1. **Flask Web Framework**: The application uses Flask as a lightweight web framework, which is ideal for this single-purpose tool where simplicity and easy customization are valuable.

2. **SQLAlchemy ORM**: Used for database interactions, providing an abstraction layer that makes database operations cleaner and more portable.

3. **SQLite Database (with option for PostgreSQL)**: The app uses SQLite by default for simplicity and ease of deployment, but is configured to support PostgreSQL via environment variables.

4. **Subprocess Management**: The application runs SQLMap as a subprocess, capturing and interpreting its output to provide real-time feedback to users.

## Key Components

### 1. Web Application (Flask)

- **app.py**: The main application file that initializes Flask, configures the database, and sets up routes.
- **main.py**: Entry point for running the application.
- **forms.py**: Contains WTForms definitions for user input validation and form handling.

### 2. Database Models

- **models.py**: Defines the database schema using SQLAlchemy ORM:
  - `Scan`: Represents a scan job with metadata such as target, status, and timestamps
  - `ScanResult`: Represents individual vulnerabilities found in a scan

### 3. SQLMap Integration

- **utils/sqlmap_manager.py**: Manages SQLMap processes, translating user options into SQLMap commands and tracking scan progress.

### 4. Frontend

- **templates/**: Contains HTML templates using Jinja2:
  - `base.html`: Base template with navigation and common structure
  - `index.html`: Home page with scan configuration form
  - `results.html`: Page for viewing scan results
- **static/**: Contains CSS and JavaScript files:
  - `css/custom.css`: Custom styling
  - `js/main.js`: Client-side functionality

## Data Flow

1. **Scan Initiation**:
   - User submits the scan form with target and options
   - Form validation occurs via Flask-WTF
   - A new Scan record is created in the database
   - SQLMapManager spawns a subprocess running SQLMap with the specified options

2. **Scan Execution**:
   - SQLMapManager runs SQLMap in a separate thread
   - Scan progress is monitored and updated in the database
   - Real-time updates are provided to the user interface

3. **Results Processing**:
   - When SQLMap finds vulnerabilities, they are parsed and stored as ScanResult records
   - Completed scans are marked with status "completed" and timestamp

4. **Results Viewing**:
   - Users can browse all scans and their detailed results
   - Results include information such as vulnerable URLs, parameters, and payloads

## External Dependencies

The application relies on the following key dependencies:

1. **Framework & Core**:
   - Flask (3.1.1+): Web framework
   - Flask-WTF (1.2.2+): Form handling and validation
   - Flask-SQLAlchemy (3.1.1+): ORM for database interactions
   - Werkzeug (3.1.3+): WSGI utilities

2. **Database**:
   - SQLAlchemy (2.0.41+): ORM toolkit
   - psycopg2-binary (2.9.10+): PostgreSQL adapter (optional)

3. **Form Validation**:
   - WTForms (3.2.1+): Form validation library
   - email-validator (2.2.0+): Email validation

4. **External Tools**:
   - SQLMap: Command-line tool for detecting SQL injection vulnerabilities
   - This is referenced in the code but apparently expected to be installed separately

5. **Frontend Libraries** (loaded from CDN):
   - Bootstrap (dark theme from Replit CDN)
   - Font Awesome
   - SweetAlert2

## Deployment Strategy

The application is configured for deployment on Replit with:

1. **Runtime Environment**:
   - Python 3.11
   - OpenSSL and PostgreSQL packages available
   - Gunicorn as the WSGI server

2. **Database Strategy**:
   - SQLite used by default for simplicity
   - Support for PostgreSQL via the DATABASE_URL environment variable
   - Connection pooling configured for production environments

3. **Process Management**:
   - Gunicorn configured to run the application with automatic reloading during development
   - Binding to 0.0.0.0:5000 to make the application publicly accessible

4. **Security Considerations**:
   - Session secret configurable via environment variable (SESSION_SECRET)
   - ProxyFix middleware to handle proxy servers correctly