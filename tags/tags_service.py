# File: `tags/tags_service.py`
from typing import Dict, Optional, Any, Union, Tuple
from pathlib import Path
import csv

class TagsService:
    """
    Load and query tags from a CSV.
    CSV expected columns: userId / user_id, movieId / movie_id, tag, timestamp
    Stores records keyed by (userId, movieId, tag).
    """

    def __init__(self, path: Optional[Union[str, Path]] = None, encoding: str = "utf-8"):
        self._tags: Dict[Tuple[int, int, str], Dict[str, Any]] = {}
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
                raw_tag = row.get("tag")
                raw_ts = row.get("timestamp") or row.get("time") or row.get("ts")

                try:
                    user_id = int(raw_user)
                    movie_id = int(raw_movie)
                    tag = (raw_tag or "").strip()
                    timestamp = int(raw_ts) if raw_ts not in (None, "") else 0
                except (TypeError, ValueError):
                    # skip rows with invalid/missing fields
                    continue

                if not tag:
                    # skip empty tags
                    continue

                key = (user_id, movie_id, tag)
                if key in self._tags:
                    # keep first occurrence
                    continue

                self._tags[key] = {
                    "userId": user_id,
                    "movieId": movie_id,
                    "tag": tag,
                    "timestamp": timestamp,
                }

    def get(self, user_id: int, movie_id: int, tag: str) -> Optional[Dict[str, Any]]:
        return self._tags.get((user_id, movie_id, tag))

    def all(self) -> Dict[Tuple[int, int, str], Dict[str, Any]]:
        return dict(self._tags)
