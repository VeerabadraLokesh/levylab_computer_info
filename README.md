# Computer Info to PSQL


## Setup
- Install python 3.11.3 on the PC for all users (Windows: https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe)
<!-- - Save Postgresql db credentials in `%APPDATA%\postgresql\pgpass.conf` on windows or on `~/.pgpass` file in Linux/Mac. [Documentation](https://www.postgresql.org/docs/current/libpq-pgpass.html) -->
- Create a new file `pgpass.conf` alongside system_info.py and save Postgresql db credentials in that file in the format `{host}:{port}:*:{username}:{password}`
<!-- - For Windows run install.bat file -->
- For Windows run install.bat file as Administrator
<!-- - For Linux run install.sh using bash -->


## Create tables in PSQL database

`psql -U {username} -d {database} -a -f create_postgres_databse.sql`

