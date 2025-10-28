import csv
import argparse
from db_setup import create_db, get_session
from links.models.db_table import LinkORM


def seed_links_from_csv(csv_path: str, commit_every: int = 1000) -> int:
    """
    Seed the `links` table from CSV.
    Empty strings in CSV are converted to None for nullable columns.
    """
    create_db()  # ensure table exists
    count = 0

    with open(csv_path, newline='', encoding='utf-8') as f, get_session() as session:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                movieId = int(row.get("movieId"))
            except (TypeError, ValueError):
                continue  # skip invalid rows

            imdbId_raw = row.get("imdbId")
            imdbId = int(imdbId_raw) if imdbId_raw and imdbId_raw.strip() else None

            tmdbId_raw = row.get("tmdbId")
            tmdbId = int(tmdbId_raw) if tmdbId_raw and tmdbId_raw.strip() else None

            link = LinkORM(movieId=movieId, imdbId=imdbId, tmdbId=tmdbId)
            session.merge(link)  # upsert

            count += 1
            if count % commit_every == 0:
                session.commit()

        session.commit()

    return count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", help="Path to links CSV file")
    parser.add_argument("--commit-every", type=int, default=1000)
    args = parser.parse_args()

    n = seed_links_from_csv(args.csv, commit_every=args.commit_every)
    print(f"Seeded {n} links from {args.csv}")

if __name__ == "__main__":
    main()
