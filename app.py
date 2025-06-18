from flask import Flask, render_template, request, abort, redirect, url_for
import csv, random, os, sqlite3
from dotenv import load_dotenv

load_dotenv()
secret_key = os.getenv("SECRET_KEY")
SECRET_PASS = os.getenv("ADMIN_PASSWORD")

app = Flask(__name__)

albums=[]
with open('files/top_500.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row["position"] = int(row["position"])
        row["date"] = int(row["date"])
        row["rating"] = float(row["rating"])
        row["num_ratings"] = int(row["num_ratings"])
        albums.append(row)

def get_albums():
    conn = sqlite3.connect('sql/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM albums ORDER BY rating DESC')
    albums = cursor.fetchall()
    conn.close()
    return albums

@app.route('/')
def index():
    page = int(request.args.get('page', 1))
    first_album = (page-1) * 100
    last_album = first_album + 100
    paginated = albums[first_album:last_album]
    total_pages = 5
    return render_template('index.html', albums=paginated, page=page, total_pages=total_pages)

@app.route('/MyTop500.html')
def my_top_500():
    my_albums = get_albums()
    per_page = 100
    page = int(request.args.get('page', 1))
    first_album = (page-1) * 100
    last_album = first_album + 100
    paginated = my_albums[first_album:last_album]
    total_pages = len(my_albums) // per_page + (len(my_albums) % per_page > 0)
    return render_template('MyTop500.html', my_albums=paginated, page=page, total_pages=total_pages)

@app.route('/album/<int:album_pos>')
def album_detail(album_pos):
    page = request.args.get('page', 1, type=int)
    source = request.args.get('source', 'index')
    album = next((a for a in albums if a["position"] == album_pos), None)
    if not album:
        abort(404)
    return render_template('album_detail.html', album=album, page=page, source=source)

@app.route('/my_album/<int:album_pos>')
def my_album_detail(album_pos):
    my_albums = get_albums()
    page = request.args.get('page', 1, type=int)
    source = request.args.get('source', 'my')
    album = next((a for a in my_albums if a["position"] == album_pos), None)
    if not album:
        abort(404)
    return render_template('my_album_detail.html', album=album, page=page, source=source)

@app.route('/random')
def random_album():
    source = request.args.get('source', 'index')
    page = request.args.get('page', 1, type=int)
    random_album = random.randint(1, 500)
    return redirect(url_for('album_detail', album_pos=random_album, source=source, page=page))

def update_pos():
    conn = sqlite3.connect("sql/database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM albums WHERE rating IS NOT NULL ORDER BY rating DESC")
    ranked_order = cursor.fetchall()

    for new_position, (album_id,) in enumerate(ranked_order, start=1):
        cursor.execute("UPDATE albums SET position = ? WHERE id = ?", (new_position, album_id))

    conn.commit()
    conn.close()

@app.route('/admin-add-review', methods = ['GET', 'POST'])
def admin_add_review():
    if request.method == 'POST':
        if request.form.get('password') != SECRET_PASS:
            return "Unauthorized", 403
        artist = request.form.get('artist')
        album = request.form.get('album')
        year = request.form.get('year') or None
        genres = request.form.get('genres')
        rating = request.form.get('rating') or None
        review = request.form.get('review')

        conn = sqlite3.connect('sql/database.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO albums (artist, album, year, genres, rating, review)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (artist, album, year, genres, rating, review))

        conn.commit()
        conn.close()
        update_pos()
        return redirect(url_for('index'))
    else:
        return render_template('admin_add_review.html')

if __name__ == '__main__':
    app.run(debug=False)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)