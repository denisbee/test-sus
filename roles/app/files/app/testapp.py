import psycopg2, json, os
from psycopg2.extras import RealDictCursor
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    with psycopg2.connect(dbname='titlesdb',
        user=os.environ.get('DB_USER', "postgres"),
        password=os.environ.get('DB_PASSWORD', ""), 
        host=os.environ.get('DB_HOST', "127.0.0.1")) as conn:
        with conn.cursor(cursor_factory = RealDictCursor) as cursor:
            genre = request.args.get('genre')
            year = request.args.get('year')
            if not genre or not year:
                return '', 204
            year = int(year)
            cursor.execute("SELECT * FROM titles WHERE genres LIKE %s AND startYear = %s ORDER BY tconst LIMIT 100", (f'%{genre}%', year))
            return json.dumps([row for row in cursor])
