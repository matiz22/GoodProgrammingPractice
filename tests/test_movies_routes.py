import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from movies.models.response import Movie


client = TestClient(app)


@pytest.fixture
def sample_movie():
    return Movie(movieId=1, title="Test Movie", genres=["Action", "Drama"])


@pytest.fixture
def sample_movies_list():
    return [
        Movie(movieId=1, title="Test Movie", genres=["Action", "Drama"]),
        Movie(movieId=2, title="Another Movie", genres=["Comedy", "Romance"])
    ]


class TestGetMovies:
    @patch('movies.routes.MoviesService.get_all')
    def test_returns_200_status(self, mock_get_all, sample_movies_list):
        mock_get_all.return_value = sample_movies_list
        response = client.get("/movies/")
        assert response.status_code == 200

    @patch('movies.routes.MoviesService.get_all')
    def test_returns_list_of_movies(self, mock_get_all, sample_movies_list):
        mock_get_all.return_value = sample_movies_list
        response = client.get("/movies/")
        assert isinstance(response.json(), list)

    @patch('movies.routes.MoviesService.get_all')
    def test_returns_correct_count(self, mock_get_all, sample_movies_list):
        mock_get_all.return_value = sample_movies_list
        response = client.get("/movies/")
        assert len(response.json()) == 2

    @patch('movies.routes.MoviesService.get_all')
    def test_returns_empty_list(self, mock_get_all):
        mock_get_all.return_value = []
        response = client.get("/movies/")
        assert response.json() == []

    @patch('movies.routes.MoviesService.get_all')
    def test_calls_service_method(self, mock_get_all, sample_movies_list):
        mock_get_all.return_value = sample_movies_list
        client.get("/movies/")
        mock_get_all.assert_called_once()


class TestGetMovie:
    @patch('movies.routes.MoviesService.get_by_id')
    def test_returns_200_when_found(self, mock_get_by_id, sample_movie):
        mock_get_by_id.return_value = sample_movie
        response = client.get("/movies/1")
        assert response.status_code == 200

    @patch('movies.routes.MoviesService.get_by_id')
    def test_returns_404_when_not_found(self, mock_get_by_id):
        mock_get_by_id.return_value = None
        response = client.get("/movies/999")
        assert response.status_code == 404

    @patch('movies.routes.MoviesService.get_by_id')
    def test_returns_movie_data(self, mock_get_by_id, sample_movie):
        mock_get_by_id.return_value = sample_movie
        response = client.get("/movies/1")
        assert response.json()["title"] == "Test Movie"

    @patch('movies.routes.MoviesService.get_by_id')
    def test_calls_service_with_correct_id(self, mock_get_by_id, sample_movie):
        mock_get_by_id.return_value = sample_movie
        client.get("/movies/42")
        mock_get_by_id.assert_called_once_with(42)

    @patch('movies.routes.MoviesService.get_by_id')
    def test_returns_error_detail(self, mock_get_by_id):
        mock_get_by_id.return_value = None
        response = client.get("/movies/999")
        assert "detail" in response.json()


class TestCreateMovie:
    @patch('movies.routes.MoviesService.create')
    def test_returns_201_status(self, mock_create, sample_movie):
        mock_create.return_value = sample_movie
        response = client.post("/movies/", json={"title": "New Movie", "genres": "Action"})
        assert response.status_code == 201

    @patch('movies.routes.MoviesService.create')
    def test_returns_created_movie(self, mock_create, sample_movie):
        mock_create.return_value = sample_movie
        response = client.post("/movies/", json={"title": "New Movie", "genres": "Action"})
        assert response.json()["movieId"] == 1

    @patch('movies.routes.MoviesService.create')
    def test_calls_service_with_data(self, mock_create, sample_movie):
        mock_create.return_value = sample_movie
        client.post("/movies/", json={"title": "New Movie", "genres": "Action"})
        mock_create.assert_called_once()

    @patch('movies.routes.MoviesService.create')
    def test_validates_request_body(self, mock_create):
        response = client.post("/movies/", json={})
        assert response.status_code == 422

    @patch('movies.routes.MoviesService.create')
    def test_returns_movie_with_all_fields(self, mock_create, sample_movie):
        mock_create.return_value = sample_movie
        response = client.post("/movies/", json={"title": "New Movie", "genres": "Action"})
        data = response.json()
        assert all(key in data for key in ["movieId", "title", "genres"])


class TestUpdateMovie:
    @patch('movies.routes.MoviesService.update')
    def test_returns_200_when_updated(self, mock_update, sample_movie):
        mock_update.return_value = sample_movie
        response = client.put("/movies/1", json={"title": "Updated"})
        assert response.status_code == 200

    @patch('movies.routes.MoviesService.update')
    def test_returns_404_when_not_found(self, mock_update):
        mock_update.return_value = None
        response = client.put("/movies/999", json={"title": "Updated"})
        assert response.status_code == 404

    @patch('movies.routes.MoviesService.update')
    def test_returns_updated_movie(self, mock_update, sample_movie):
        mock_update.return_value = sample_movie
        response = client.put("/movies/1", json={"title": "Updated"})
        assert "movieId" in response.json()

    @patch('movies.routes.MoviesService.update')
    def test_calls_service_with_id_and_data(self, mock_update, sample_movie):
        mock_update.return_value = sample_movie
        client.put("/movies/42", json={"title": "Updated"})
        assert mock_update.call_args[0][0] == 42

    @patch('movies.routes.MoviesService.update')
    def test_accepts_partial_updates(self, mock_update, sample_movie):
        mock_update.return_value = sample_movie
        response = client.put("/movies/1", json={"title": "Only Title"})
        assert response.status_code == 200


class TestDeleteMovie:
    @patch('movies.routes.MoviesService.delete')
    def test_returns_204_when_deleted(self, mock_delete):
        mock_delete.return_value = True
        response = client.delete("/movies/1")
        assert response.status_code == 204

    @patch('movies.routes.MoviesService.delete')
    def test_returns_404_when_not_found(self, mock_delete):
        mock_delete.return_value = False
        response = client.delete("/movies/999")
        assert response.status_code == 404

    @patch('movies.routes.MoviesService.delete')
    def test_calls_service_with_correct_id(self, mock_delete):
        mock_delete.return_value = True
        client.delete("/movies/42")
        mock_delete.assert_called_once_with(42)

    @patch('movies.routes.MoviesService.delete')
    def test_returns_no_content(self, mock_delete):
        mock_delete.return_value = True
        response = client.delete("/movies/1")
        assert response.content == b''

    @patch('movies.routes.MoviesService.delete')
    def test_returns_error_detail_when_not_found(self, mock_delete):
        mock_delete.return_value = False
        response = client.delete("/movies/999")
        assert "detail" in response.json()

