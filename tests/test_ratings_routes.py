import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from ratings.models.response import Rating


client = TestClient(app)


@pytest.fixture
def sample_rating():
    return Rating(userId=1, movieId=100, rating=4.5, timestamp=1234567890)


@pytest.fixture
def sample_ratings_list():
    return [
        Rating(userId=1, movieId=100, rating=4.5, timestamp=1234567890),
        Rating(userId=2, movieId=101, rating=3.5, timestamp=1234567891)
    ]


class TestGetRatings:
    @patch('ratings.routes.RatingsService.get_all')
    def test_returns_200_status(self, mock_get_all, sample_ratings_list):
        mock_get_all.return_value = sample_ratings_list
        response = client.get("/ratings/")
        assert response.status_code == 200

    @patch('ratings.routes.RatingsService.get_all')
    def test_returns_list_of_ratings(self, mock_get_all, sample_ratings_list):
        mock_get_all.return_value = sample_ratings_list
        response = client.get("/ratings/")
        assert isinstance(response.json(), list)

    @patch('ratings.routes.RatingsService.get_all')
    def test_returns_correct_count(self, mock_get_all, sample_ratings_list):
        mock_get_all.return_value = sample_ratings_list
        response = client.get("/ratings/")
        assert len(response.json()) == 2

    @patch('ratings.routes.RatingsService.get_all')
    def test_returns_empty_list(self, mock_get_all):
        mock_get_all.return_value = []
        response = client.get("/ratings/")
        assert response.json() == []

    @patch('ratings.routes.RatingsService.get_all')
    def test_calls_service_method(self, mock_get_all, sample_ratings_list):
        mock_get_all.return_value = sample_ratings_list
        client.get("/ratings/")
        mock_get_all.assert_called_once()


class TestGetRating:
    @patch('ratings.routes.RatingsService.get_by_user_and_movie')
    def test_returns_200_when_found(self, mock_get_by_user_and_movie, sample_rating):
        mock_get_by_user_and_movie.return_value = sample_rating
        response = client.get("/ratings/1/100")
        assert response.status_code == 200

    @patch('ratings.routes.RatingsService.get_by_user_and_movie')
    def test_returns_404_when_not_found(self, mock_get_by_user_and_movie):
        mock_get_by_user_and_movie.return_value = None
        response = client.get("/ratings/999/999")
        assert response.status_code == 404

    @patch('ratings.routes.RatingsService.get_by_user_and_movie')
    def test_returns_rating_data(self, mock_get_by_user_and_movie, sample_rating):
        mock_get_by_user_and_movie.return_value = sample_rating
        response = client.get("/ratings/1/100")
        assert response.json()["rating"] == 4.5

    @patch('ratings.routes.RatingsService.get_by_user_and_movie')
    def test_calls_service_with_correct_ids(self, mock_get_by_user_and_movie, sample_rating):
        mock_get_by_user_and_movie.return_value = sample_rating
        client.get("/ratings/42/123")
        mock_get_by_user_and_movie.assert_called_once_with(42, 123)

    @patch('ratings.routes.RatingsService.get_by_user_and_movie')
    def test_returns_error_detail(self, mock_get_by_user_and_movie):
        mock_get_by_user_and_movie.return_value = None
        response = client.get("/ratings/999/999")
        assert "detail" in response.json()


class TestCreateRating:
    @patch('ratings.routes.RatingsService.create')
    def test_returns_201_status(self, mock_create, sample_rating):
        mock_create.return_value = sample_rating
        response = client.post("/ratings/", json={"userId": 1, "movieId": 100, "rating": 4.5, "timestamp": 1234567890})
        assert response.status_code == 201

    @patch('ratings.routes.RatingsService.create')
    def test_returns_created_rating(self, mock_create, sample_rating):
        mock_create.return_value = sample_rating
        response = client.post("/ratings/", json={"userId": 1, "movieId": 100, "rating": 4.5, "timestamp": 1234567890})
        assert response.json()["userId"] == 1

    @patch('ratings.routes.RatingsService.create')
    def test_calls_service_with_data(self, mock_create, sample_rating):
        mock_create.return_value = sample_rating
        client.post("/ratings/", json={"userId": 1, "movieId": 100, "rating": 4.5, "timestamp": 1234567890})
        mock_create.assert_called_once()

    @patch('ratings.routes.RatingsService.create')
    def test_validates_request_body(self, mock_create):
        response = client.post("/ratings/", json={})
        assert response.status_code == 422

    @patch('ratings.routes.RatingsService.create')
    def test_validates_rating_range(self, mock_create):
        response = client.post("/ratings/", json={"userId": 1, "movieId": 100, "rating": 6.0})
        assert response.status_code == 422


class TestUpdateRating:
    @patch('ratings.routes.RatingsService.update')
    def test_returns_200_when_updated(self, mock_update, sample_rating):
        mock_update.return_value = sample_rating
        response = client.put("/ratings/1/100", json={"rating": 5.0})
        assert response.status_code == 200

    @patch('ratings.routes.RatingsService.update')
    def test_returns_404_when_not_found(self, mock_update):
        mock_update.return_value = None
        response = client.put("/ratings/999/999", json={"rating": 5.0})
        assert response.status_code == 404

    @patch('ratings.routes.RatingsService.update')
    def test_returns_updated_rating(self, mock_update, sample_rating):
        mock_update.return_value = sample_rating
        response = client.put("/ratings/1/100", json={"rating": 5.0})
        assert "userId" in response.json()

    @patch('ratings.routes.RatingsService.update')
    def test_calls_service_with_ids_and_data(self, mock_update, sample_rating):
        mock_update.return_value = sample_rating
        client.put("/ratings/42/123", json={"rating": 5.0})
        assert mock_update.call_args[0][0] == 42
        assert mock_update.call_args[0][1] == 123

    @patch('ratings.routes.RatingsService.update')
    def test_validates_rating_range(self, mock_update):
        response = client.put("/ratings/1/100", json={"rating": 6.0})
        assert response.status_code == 422


class TestDeleteRating:
    @patch('ratings.routes.RatingsService.delete')
    def test_returns_204_when_deleted(self, mock_delete):
        mock_delete.return_value = True
        response = client.delete("/ratings/1/100")
        assert response.status_code == 204

    @patch('ratings.routes.RatingsService.delete')
    def test_returns_404_when_not_found(self, mock_delete):
        mock_delete.return_value = False
        response = client.delete("/ratings/999/999")
        assert response.status_code == 404

    @patch('ratings.routes.RatingsService.delete')
    def test_calls_service_with_correct_ids(self, mock_delete):
        mock_delete.return_value = True
        client.delete("/ratings/42/123")
        mock_delete.assert_called_once_with(42, 123)

    @patch('ratings.routes.RatingsService.delete')
    def test_returns_no_content(self, mock_delete):
        mock_delete.return_value = True
        response = client.delete("/ratings/1/100")
        assert response.content == b''

    @patch('ratings.routes.RatingsService.delete')
    def test_returns_error_detail_when_not_found(self, mock_delete):
        mock_delete.return_value = False
        response = client.delete("/ratings/999/999")
        assert "detail" in response.json()

