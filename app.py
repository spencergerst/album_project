from flask import Flask, render_template, request, abort, redirect, url_for
import csv, random, os
from dotenv import load_dotenv

load_dotenv()
secret_key = os.getenv("SECRET_KEY")


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

my_albums=[]
with open('files/my_top_500.csv', newline='', encoding='utf-8-sig') as csvfile:
    my_album_reader = csv.DictReader(csvfile)
    for row in my_album_reader:
        row["position"] = int(row["position"])
        row["date"] = int(row["date"])
        row["rating"] = float(row["rating"])
        row["num_ratings"] = int(row["num_ratings"])
        my_albums.append(row)

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

if __name__ == '__main__':
    app.run(debug=False)