import csv
import argparse

from db_setup import create_db, get_session
from movies.models.response import (Movie as MovieSchema)
from movies.models.db_table import MovieORM

def seed_from_csv(csv_path: str, commit_every: int = 1000) -> int:
    create_db()
    count = 0
    with open(csv_path, newline='', encoding='utf-8') as f, get_session() as session:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                movie_id = int(row.get("movieId") or row.get("movie_id") or row.get("id"))
            except Exception:
                continue

            title = (row.get("title") or "").strip()
            genres_raw = row.get("genres", "")
            genres = [g.strip() for g in genres_raw.split("|") if g.strip()]

            movie = MovieSchema(movieId=movie_id, title=title, genres=genres)

            orm_obj = MovieORM(movieId=movie.movieId, title=movie.title, genres=movie.genres)
            session.merge(orm_obj)

            count += 1
            if count % commit_every == 0:
                session.commit()

        session.commit()
    return count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", help="Path to CSV file")
    parser.add_argument("--commit-every", type=int, default=1000)
    args = parser.parse_args()
    csv_path = args.csv
    n = seed_from_csv(csv_path, commit_every=args.commit_every)
    print(f"Seeded {n} rows from {csv_path}")

if __name__ == "__main__":
    main()
