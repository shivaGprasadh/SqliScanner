# SQLi Scanner - Detailed Installation Guide

This document provides detailed step-by-step instructions for installing and configuring the SQLi Scanner application.

## Required Dependencies

The application requires the following packages:
- email-validator (2.2.0)
- flask (3.1.1)
- flask-sqlalchemy (3.1.1)
- flask-wtf (1.2.2)
- gunicorn (23.0.0)
- psycopg2-binary (2.9.10)
- sqlalchemy (2.0.41)
- werkzeug (3.1.3)
- wtforms (3.2.1)

## Installing SQLMap

SQLMap is required for the scanner to function. Follow the instructions below for your operating system:

### Mac OS

```bash
# Using Homebrew
brew install sqlmap

# Verify installation
sqlmap --version
```

### Linux (Debian/Ubuntu)

```bash
# Using apt package manager
sudo apt-get update
sudo apt-get install sqlmap

# Verify installation
sqlmap --version
```

### Linux (Fedora)

```bash
# Using dnf package manager
sudo dnf install sqlmap

# Verify installation
sqlmap --version
```

### Linux (Arch)

```bash
# Using pacman package manager
sudo pacman -S sqlmap

# Verify installation
sqlmap --version
```

### Manual Installation (All platforms)

If the package manager installation doesn't work, you can install SQLMap manually:

```bash
# Clone the SQLMap repository
git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git

# Add to PATH (add this to your .bashrc or .zshrc file)
export PATH=$PATH:/path/to/sqlmap
```

## Database Configuration

### SQLite (Default)

SQLite is used by default and requires no additional setup. The database file will be created in the project directory as `sqliscanner.db`.

### PostgreSQL Setup

1. Install PostgreSQL:

   **Mac OS**:
   ```bash
   brew install postgresql
   brew services start postgresql
   ```

   **Debian/Ubuntu**:
   ```bash
   sudo apt-get install postgresql postgresql-contrib
   sudo systemctl start postgresql
   ```

   **Fedora**:
   ```bash
   sudo dnf install postgresql postgresql-server
   sudo postgresql-setup --initdb
   sudo systemctl start postgresql
   ```

   **Arch Linux**:
   ```bash
   sudo pacman -S postgresql
   sudo -u postgres initdb -D /var/lib/postgres/data
   sudo systemctl start postgresql
   ```

2. Create a database and user:

   ```bash
   sudo -u postgres psql
   ```

   In the PostgreSQL prompt:
   ```sql
   CREATE DATABASE sqli_scanner;
   CREATE USER sqli_user WITH ENCRYPTED PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE sqli_scanner TO sqli_user;
   \q
   ```

3. Configure the application to use PostgreSQL by setting the DATABASE_URL environment variable:

   ```bash
   export DATABASE_URL=postgresql://sqli_user:your_password@localhost/sqli_scanner
   ```

## Application Configuration

1. Environment Variables:

   Create a `.env` file in the project root with the following content:

   ```
   # Database configuration (optional, SQLite is used by default)
   DATABASE_URL=postgresql://sqli_user:your_password@localhost/sqli_scanner

   # Session security (required)
   SESSION_SECRET=your_secret_key

   # SQLMap path (if not in system PATH)
   SQLMAP_PATH=/path/to/sqlmap
   ```

2. Configure the SQLMap path (if needed):

   If SQLMap is not in your system PATH, edit the `utils/sqlmap_manager.py` file and update the `sqlmap_path` variable:

   ```python
   self.sqlmap_path = "/path/to/your/sqlmap"
   ```

## Troubleshooting

### SQLMap Not Found

If you encounter the error "SQLMap check failed: [Errno 2] No such file or directory: 'sqlmap'", it means SQLMap is not properly installed or not in your PATH.

Solutions:
1. Install SQLMap using your package manager
2. Install SQLMap manually and update the PATH
3. Update the `sqlmap_path` variable in `utils/sqlmap_manager.py` with the full path to the SQLMap executable

### Database Connection Issues

If you encounter database connection errors:

1. For SQLite:
   - Ensure the application has write permissions to the project directory
   - Check for disk space issues

2. For PostgreSQL:
   - Verify the PostgreSQL service is running
   - Confirm the database and user exist with proper permissions
   - Check the DATABASE_URL environment variable is correctly set
   - Ensure psycopg2-binary is installed

### Port Already in Use

If you see "Address already in use" when starting the application:

```bash
# Find the process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or start the application on a different port
gunicorn --bind 0.0.0.0:5001 --reuse-port --reload main:app
```

## Getting Help

For more information about SQLMap and its options, visit the official website:
https://sqlmap.org/

For detailed documentation on all SQLMap parameters:
https://github.com/sqlmapproject/sqlmap/wiki/Usage