# Full Text Search with React, Flask and PostgreSQL

## Setup Database

### Run Postgres as Docker Container

```bash
cd database
docker-compose up -d
```

### Connect to PostgreSQL with psql (PostgreSQL interactive terminal)

```bash
docker-compose run db bash
psql --host=db --username=${POSTGRES_USER} --dbname=${POSTGRES_DB}
```

Enter your **password** for admin user.

### Import `netflix_titles.csv` in `show` table.

The list was published by Shivam Bansal on [kaggle.com](https://www.kaggle.com/shivamb/netflix-shows) and contains 6234 titles of Netflix Movies and TV Shows.

```SQL
COPY show (id, type, title, director, actors, country, date_added, release_year, rating, duration, listed_in, description) FROM '/data/netflix_titles.csv' CSV HEADER;
>> COPY 6234
```

Enter `\q` to exit psql.

### Connect to `netflix` database

```bash
\c netflix
>> You are now connected to database "netflix" as user "admin".
```

> To stop the PostgreSQL Container execute `docker-compose down`.

## Setup Python Flask Server

### Create Python Environment

```bash
cd server
python3 -m venv venv
source venv/bin/activate
```

### Install Python Modules

```bash
pip install Flask
pip install flask-sqlalchemy
pip install Flask-Migrate
pip install psycopg2-binary
```

### Set Flask Environment Variables

```bash
export FLASK_APP=server.py
export FLASK_ENV=development
```

### Start Flask Server

```bash
flask run
```

### Migrate Database with Flask-Migrate

Create a Migration Script

```bash
flask db migrate -m "migration message"
```

Upgrading the Database

```bash
flask db upgrade
```

## Setup Client in Development Mode

```bash
cd client
npm start
```

Open [http://localhost:3000/](http://localhost:3000/) to see the search bar.