from typing import Dict, List, Optional, Union, Any
from pathlib import Path
import csv

class MoviesService:
    """
    Service to load and query movies from a CSV.
    CSV expected to have columns: movieId / movie_id / id, title, genres
    """

    def __init__(self, path: Optional[Union[str, Path]] = None, encoding: str = "utf-8"):
        self._movies: Dict[int, Dict[str, Any]] = {}
        self._encoding = encoding
        if path is not None:
            self.load_from_csv(path)

    @staticmethod
    def _parse_genres(genres_str: Optional[str]) -> List[str]:
        if not genres_str:
            return []
        return [g.strip() for g in genres_str.split("|") if g.strip()]

    def load_from_csv(self, path: Union[str, Path]) -> None:
        path = Path(path)
        with path.open(newline="", encoding=self._encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                raw_id = row.get("movieId") or row.get("movie_id") or row.get("id")
                try:
                    movie_id = int(raw_id)
                except (TypeError, ValueError):
                    continue  # skip rows with missing/invalid id

                if movie_id in self._movies:
                    continue  # keep first occurrence, skip duplicates

                title = (row.get("title") or "").strip()
                genres = self._parse_genres(row.get("genres") or "")
                self._movies[movie_id] = {"movieId": movie_id, "title": title, "genres": genres}

    def get(self, movie_id: int) -> Optional[Dict[str, Any]]:
        return self._movies.get(movie_id)

    def all(self) -> Dict[int, Dict[str, Any]]:
        return dict(self._movies)
