# SQLi Scanner

A Flask-based SQL injection vulnerability scanner web application that integrates with SQLMap to scan websites for SQL injection vulnerabilities.

## Features

- User-friendly web interface for SQLMap
- Domain crawling and targeted URL scanning
- Real-time scan progress monitoring
- Comprehensive results viewing
- Advanced vulnerability detection options
- Database information extraction capabilities
- User and password enumeration features

## Screenshots

| Scan Configuration | Results Viewing |
|:-------------------:|:----------------:|
| ![Scan Configuration](https://via.placeholder.com/400x300?text=Scan+Configuration) | ![Results View](https://via.placeholder.com/400x300?text=Results+View) |

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- SQLMap
- PostgreSQL (optional, SQLite is used by default)

### Mac OS Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sqli-scanner.git
   cd sqli-scanner
   ```

2. Install SQLMap:
   ```
   brew install sqlmap
   ```

3. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set up environment variables (optional for PostgreSQL):
   ```
   export DATABASE_URL=postgresql://username:password@localhost/sqli_scanner
   export SESSION_SECRET=your_secret_key
   ```

### Linux Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sqli-scanner.git
   cd sqli-scanner
   ```

2. Install SQLMap:
   ```
   # Debian/Ubuntu
   sudo apt-get update
   sudo apt-get install sqlmap
   
   # Fedora
   sudo dnf install sqlmap
   
   # Arch Linux
   sudo pacman -S sqlmap
   ```

3. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set up environment variables (optional for PostgreSQL):
   ```
   export DATABASE_URL=postgresql://username:password@localhost/sqli_scanner
   export SESSION_SECRET=your_secret_key
   ```

## Database Setup

### Using SQLite (Default)

No additional configuration needed. The application will create a SQLite database file named `sqliscanner.db` in the project directory.

### Using PostgreSQL

1. Install PostgreSQL:
   ```
   # Mac OS
   brew install postgresql
   brew services start postgresql
   
   # Debian/Ubuntu
   sudo apt-get install postgresql postgresql-contrib
   sudo systemctl start postgresql
   
   # Fedora
   sudo dnf install postgresql postgresql-server
   sudo systemctl start postgresql
   
   # Arch Linux
   sudo pacman -S postgresql
   sudo systemctl start postgresql
   ```

2. Create a database and user:
   ```
   sudo -u postgres psql
   
   CREATE DATABASE sqli_scanner;
   CREATE USER sqli_user WITH ENCRYPTED PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE sqli_scanner TO sqli_user;
   \q
   ```

3. Set the DATABASE_URL environment variable:
   ```
   export DATABASE_URL=postgresql://sqli_user:your_password@localhost/sqli_scanner
   ```

## Running the Application

1. Start the application:
   ```
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. **Select Target Type**:
   - **Specific URL**: To scan a single URL
   - **Domain**: To crawl and scan an entire website

2. **Enter Target**:
   - For specific URL: Enter complete URL with parameters (e.g., https://example.com/page.php?id=1)
   - For domain: Enter domain name (e.g., example.com)

3. **Configure Options**:
   - **Basic Options**: Crawl depth, form testing
   - **Detection Options**: Level and risk
   - **Injection Options**: SQL injection techniques, tamper scripts
   - **Request Options**: HTTP headers, cookies
   - **Enumeration Options**: Database structure extraction
   - **Advanced Options**: Thread count, timeout, OS shell attempts

4. **Start Scan** and monitor progress in real-time

5. **View Results** in the Results tab

## Requirements.txt

```
email-validator==2.2.0
flask==3.1.1
flask-sqlalchemy==3.1.1
flask-wtf==1.2.2
gunicorn==23.0.0
psycopg2-binary==2.9.10
sqlalchemy==2.0.41
werkzeug==3.1.3
wtforms==3.2.1
```

## Ethical Use Disclaimer

This tool is designed for security professionals and website administrators to test their own websites for SQL injection vulnerabilities. Always obtain proper authorization before scanning any website. Unauthorized scanning of websites is illegal and unethical.

## License

This project is licensed under the MIT License - see the LICENSE file for details.