from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.sql.expression import func
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
    tsv_searchable_text = db.Column(TSVECTOR)

    __table_args__ = (db.Index('tsv_idx', 'tsv_searchable_text', postgresql_using = 'gin'),)

    def __repr__(self):
        return f'<Show {self.title}>'

function_snippet = db.DDL("""
    CREATE FUNCTION tsv_searchable_text_trigger() RETURNS trigger AS $$
    begin
    new.tsv_searchable_text :=
        setweight(to_tsvector('pg_catalog.english', coalesce(new.title,'')), 'A') ||
        setweight(to_tsvector('pg_catalog.english', coalesce(new.description,'')), 'B') ||
        setweight(to_tsvector('pg_catalog.english', coalesce(new.director,'')), 'C') ||
        setweight(to_tsvector('pg_catalog.english', coalesce(new.actors,'')), 'C');
    return new;
    end
    $$ LANGUAGE plpgsql;
""")
    
trigger_snippet = db.DDL("""
    CREATE TRIGGER searchable_text_update BEFORE INSERT OR UPDATE
    ON show
    FOR EACH ROW EXECUTE PROCEDURE tsv_searchable_text_trigger();
""")

db.event.listen(Show.__table__, 'after_create', function_snippet.execute_if(dialect = 'postgresql'))
db.event.listen(Show.__table__, 'after_create', trigger_snippet.execute_if(dialect = 'postgresql'))


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

@app.route('/search')
def search():
    search_query = request.args.get('search')
    search_query = search_query.replace(" ", "&")
    shows = db.session.query(
        Show.id,
        Show.title,
        Show.description,
        func.ts_rank_cd(Show.tsv_searchable_text, func.plainto_tsquery(search_query, postgresql_regconfig='english'), 32).label('rank')
    ).filter(
        Show.tsv_searchable_text.match(search_query, postgresql_regconfig='english')
    ).order_by(db.text('rank DESC')).limit(10)

    data = []
    for show in shows:
        data.append({
            'id': show.id,
            'title': show.title,
            'description': show.description,
            'rank': show.rank
        })
    return jsonify(data)

@app.route('/create-tables')
def create_tables():
    db.drop_all()
    db.create_all()
    return {'success': True}