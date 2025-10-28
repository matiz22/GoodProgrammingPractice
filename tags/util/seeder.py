import csv
import argparse

from db_setup import create_db, get_session
from tags.models.db_table import TagORM


def seed_tags_from_csv(csv_path: str, commit_every: int = 1000) -> int:
    """
    Seed the `tags` table from CSV.
    Expects columns: userId,movieId,tag,timestamp
    """
    create_db()
    count = 0

    with open(csv_path, newline='', encoding='utf-8') as f, get_session() as session:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                userId = int(row.get("userId"))
                movieId = int(row.get("movieId"))
                tag_text = row.get("tag").strip()
                timestamp = int(row.get("timestamp") or 0)
            except (TypeError, ValueError, AttributeError):
                continue  # skip invalid rows

            tag_obj = TagORM(userId=userId, movieId=movieId, tag=tag_text, timestamp=timestamp)
            session.merge(tag_obj)  # upsert
            count += 1

            if count % commit_every == 0:
                session.commit()

        session.commit()

    return count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", help="Path to tags CSV file")
    parser.add_argument("--commit-every", type=int, default=1000)
    args = parser.parse_args()

    n = seed_tags_from_csv(args.csv, commit_every=args.commit_every)
    print(f"Seeded {n} tags from {args.csv}")

if __name__ == "__main__":
    main()
