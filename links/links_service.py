from typing import Dict, Optional, Any, Union
from pathlib import Path
import csv

class LinksService:
    """
    Load and query links from a CSV.
    CSV expected columns: movieId / movie_id / id, imdbId, tmdbId
    """

    def __init__(self, path: Optional[Union[str, Path]] = None, encoding: str = "utf-8"):
        self._links: Dict[int, Dict[str, Any]] = {}
        self._encoding = encoding
        if path is not None:
            self.load_from_csv(path)

    def load_from_csv(self, path: Union[str, Path]) -> None:
        path = Path(path)
        with path.open(newline="", encoding=self._encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                raw_id = row.get("movieId") or row.get("movie_id") or row.get("id")
                try:
                    movie_id = int(raw_id)
                except (TypeError, ValueError):
                    continue  # skip invalid/missing ids

                if movie_id in self._links:
                    continue  # keep first occurrence

                imdb_id = (row.get("imdbId") or row.get("imdb_id") or "").strip()
                tmdb_id = (row.get("tmdbId") or row.get("tmdb_id") or "").strip()

                self._links[movie_id] = {
                    "movieId": movie_id,
                    "imdbId": imdb_id,
                    "tmdbId": tmdb_id,
                }

    def get(self, movie_id: int) -> Optional[Dict[str, Any]]:
        return self._links.get(movie_id)

    def all(self) -> Dict[int, Dict[str, Any]]:
        return dict(self._links)
