from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://admin:badsecret@127.0.0.1:5432/netflix'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))
    title = db.Column(db.Text)
    director = db.Column(db.Text)
    actors = db.Column(db.Text)
    country = db.Column(db.Text)
    date_added = db.Column(db.Date)
    release_year = db.Column(db.Integer)
    rating = db.Column(db.String(10))
    duration = db.Column(db.String(10))
    listed_in = db.Column(db.Text)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Show {self.title}>'

@app.route('/')
def shows():
    shows = Show.query.limit(10)
    data = []
    for show in shows:
        data.append({
            'id': show.id,
            'type': show.type,
            'title': show.title,
            'director': show.director,
            'actors': show.actors,
            'country': show.country,
            'date_added': show.date_added,
            'release_year': show.release_year,
            'rating' : show.rating,
            'duration': show.duration,
            'listed_in': show.listed_in,
            'description': show.description
        })
    return jsonify(data)