import csv
import argparse

from db_setup import create_db, get_session
from ratings.models.db_table import RatingORM


def seed_ratings_from_csv(csv_path: str, commit_every: int = 1000) -> int:
    """
    Seed the `ratings` table from CSV.
    Expects columns: userId,movieId,rating,timestamp
    """
    create_db()
    count = 0

    with open(csv_path, newline='', encoding='utf-8') as f, get_session() as session:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                userId = int(row.get("userId"))
                movieId = int(row.get("movieId"))
                rating = float(row.get("rating"))
                timestamp = int(row.get("timestamp") or 0)
            except (TypeError, ValueError):
                continue

            rating_obj = RatingORM(userId=userId, movieId=movieId, rating=rating, timestamp=timestamp)
            session.merge(rating_obj)  # upsert
            count += 1

            if count % commit_every == 0:
                session.commit()

        session.commit()

    return count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", help="Path to ratings CSV file")
    parser.add_argument("--commit-every", type=int, default=1000)
    args = parser.parse_args()

    n = seed_ratings_from_csv(args.csv, commit_every=args.commit_every)
    print(f"Seeded {n} ratings from {args.csv}")

if __name__ == "__main__":
    main()
