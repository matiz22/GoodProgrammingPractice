from typing import Dict, Optional, Any, Union, Tuple
from pathlib import Path
import csv

class RatingsService:
    """
    Load and query ratings from a CSV.
    CSV expected columns: userId / user_id, movieId / movie_id, rating, timestamp
    Stores records keyed by (userId, movieId).
    """

    def __init__(self, path: Optional[Union[str, Path]] = None, encoding: str = "utf-8"):
        self._ratings: Dict[Tuple[int, int], Dict[str, Any]] = {}
        self._encoding = encoding
        if path is not None:
            self.load_from_csv(path)

    def load_from_csv(self, path: Union[str, Path]) -> None:
        path = Path(path)
        with path.open(newline="", encoding=self._encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                raw_user = row.get("userId") or row.get("user_id") or row.get("user")
                raw_movie = row.get("movieId") or row.get("movie_id") or row.get("movie")
                raw_rating = row.get("rating")
                raw_ts = row.get("timestamp") or row.get("time") or row.get("ts")

                try:
                    user_id = int(raw_user)
                    movie_id = int(raw_movie)
                    rating = float(raw_rating)
                    timestamp = int(raw_ts) if raw_ts not in (None, "") else 0
                except (TypeError, ValueError):
                    # skip rows with invalid/missing fields
                    continue

                key = (user_id, movie_id)
                if key in self._ratings:
                    # keep first occurrence, skip duplicates
                    continue

                self._ratings[key] = {
                    "userId": user_id,
                    "movieId": movie_id,
                    "rating": rating,
                    "timestamp": timestamp,
                }

    def get(self, user_id: int, movie_id: int) -> Optional[Dict[str, Any]]:
        return self._ratings.get((user_id, movie_id))

    def all(self) -> Dict[Tuple[int, int], Dict[str, Any]]:
        return dict(self._ratings)
