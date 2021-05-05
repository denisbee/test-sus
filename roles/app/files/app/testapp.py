import psycopg2, json
from psycopg2.extras import RealDictCursor
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    with psycopg2.connect(dbname='titlesdb', user='testuser',  password='testpasswd1', host='192.168.88.82') as conn:
        with conn.cursor(cursor_factory = RealDictCursor) as cursor:
            genre = request.args.get('genre')
            year = request.args.get('year')
            if not genre or not year:
                return '', 204
            year = int(year)
            cursor.execute("SELECT * FROM titles WHERE genres LIKE %s AND startYear = %s limit 100", (f'%{genre}%', year))
            return json.dumps([row for row in cursor])
