import sqlite3, csv

conn = sqlite3.connect('sql/database.db')
cursor = conn.cursor()

with open('files/my_top_500.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute('''
            INSERT INTO albums (position, artist, album, year, genres, rating, review)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            int(row["position"]),
            row["artist"],
            row["name"],
            int(row["date"]) if row["date"] else None,
            row.get("genres", ""),
            float(row["rating"]) if "rating" in row and row["rating"] else None,
            row.get("review", "")
        ))
conn.commit()
conn.close()
