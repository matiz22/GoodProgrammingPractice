import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from tags.models.response import Tag


client = TestClient(app)


@pytest.fixture
def sample_tag():
    return Tag(userId=1, movieId=100, tag="great movie", timestamp=1234567890)


@pytest.fixture
def sample_tags_list():
    return [
        Tag(userId=1, movieId=100, tag="great movie", timestamp=1234567890),
        Tag(userId=2, movieId=101, tag="awesome", timestamp=1234567891)
    ]


class TestGetTags:
    @patch('tags.routes.TagsService.get_all')
    def test_returns_200_status(self, mock_get_all, sample_tags_list):
        mock_get_all.return_value = sample_tags_list
        response = client.get("/tags/")
        assert response.status_code == 200

    @patch('tags.routes.TagsService.get_all')
    def test_returns_list_of_tags(self, mock_get_all, sample_tags_list):
        mock_get_all.return_value = sample_tags_list
        response = client.get("/tags/")
        assert isinstance(response.json(), list)

    @patch('tags.routes.TagsService.get_all')
    def test_returns_correct_count(self, mock_get_all, sample_tags_list):
        mock_get_all.return_value = sample_tags_list
        response = client.get("/tags/")
        assert len(response.json()) == 2

    @patch('tags.routes.TagsService.get_all')
    def test_returns_empty_list(self, mock_get_all):
        mock_get_all.return_value = []
        response = client.get("/tags/")
        assert response.json() == []

    @patch('tags.routes.TagsService.get_all')
    def test_calls_service_method(self, mock_get_all, sample_tags_list):
        mock_get_all.return_value = sample_tags_list
        client.get("/tags/")
        mock_get_all.assert_called_once()


class TestGetTag:
    @patch('tags.routes.TagsService.get_by_user_and_movie')
    def test_returns_200_when_found(self, mock_get_by_user_and_movie, sample_tag):
        mock_get_by_user_and_movie.return_value = sample_tag
        response = client.get("/tags/1/100")
        assert response.status_code == 200

    @patch('tags.routes.TagsService.get_by_user_and_movie')
    def test_returns_404_when_not_found(self, mock_get_by_user_and_movie):
        mock_get_by_user_and_movie.return_value = None
        response = client.get("/tags/999/999")
        assert response.status_code == 404

    @patch('tags.routes.TagsService.get_by_user_and_movie')
    def test_returns_tag_data(self, mock_get_by_user_and_movie, sample_tag):
        mock_get_by_user_and_movie.return_value = sample_tag
        response = client.get("/tags/1/100")
        assert response.json()["tag"] == "great movie"

    @patch('tags.routes.TagsService.get_by_user_and_movie')
    def test_calls_service_with_correct_ids(self, mock_get_by_user_and_movie, sample_tag):
        mock_get_by_user_and_movie.return_value = sample_tag
        client.get("/tags/42/123")
        mock_get_by_user_and_movie.assert_called_once_with(42, 123)

    @patch('tags.routes.TagsService.get_by_user_and_movie')
    def test_returns_error_detail(self, mock_get_by_user_and_movie):
        mock_get_by_user_and_movie.return_value = None
        response = client.get("/tags/999/999")
        assert "detail" in response.json()


class TestCreateTag:
    @patch('tags.routes.TagsService.create')
    def test_returns_201_status(self, mock_create, sample_tag):
        mock_create.return_value = sample_tag
        response = client.post("/tags/", json={"userId": 1, "movieId": 100, "tag": "great movie", "timestamp": 1234567890})
        assert response.status_code == 201

    @patch('tags.routes.TagsService.create')
    def test_returns_created_tag(self, mock_create, sample_tag):
        mock_create.return_value = sample_tag
        response = client.post("/tags/", json={"userId": 1, "movieId": 100, "tag": "great movie", "timestamp": 1234567890})
        assert response.json()["userId"] == 1

    @patch('tags.routes.TagsService.create')
    def test_calls_service_with_data(self, mock_create, sample_tag):
        mock_create.return_value = sample_tag
        client.post("/tags/", json={"userId": 1, "movieId": 100, "tag": "great movie", "timestamp": 1234567890})
        mock_create.assert_called_once()

    @patch('tags.routes.TagsService.create')
    def test_validates_request_body(self, mock_create):
        response = client.post("/tags/", json={})
        assert response.status_code == 422

    @patch('tags.routes.TagsService.create')
    def test_returns_tag_with_all_fields(self, mock_create, sample_tag):
        mock_create.return_value = sample_tag
        response = client.post("/tags/", json={"userId": 1, "movieId": 100, "tag": "great movie"})
        data = response.json()
        assert all(key in data for key in ["userId", "movieId", "tag", "timestamp"])


class TestUpdateTag:
    @patch('tags.routes.TagsService.update')
    def test_returns_200_when_updated(self, mock_update, sample_tag):
        mock_update.return_value = sample_tag
        response = client.put("/tags/1/100", json={"tag": "updated tag"})
        assert response.status_code == 200

    @patch('tags.routes.TagsService.update')
    def test_returns_404_when_not_found(self, mock_update):
        mock_update.return_value = None
        response = client.put("/tags/999/999", json={"tag": "updated tag"})
        assert response.status_code == 404

    @patch('tags.routes.TagsService.update')
    def test_returns_updated_tag(self, mock_update, sample_tag):
        mock_update.return_value = sample_tag
        response = client.put("/tags/1/100", json={"tag": "updated tag"})
        assert "userId" in response.json()

    @patch('tags.routes.TagsService.update')
    def test_calls_service_with_ids_and_data(self, mock_update, sample_tag):
        mock_update.return_value = sample_tag
        client.put("/tags/42/123", json={"tag": "updated tag"})
        assert mock_update.call_args[0][0] == 42
        assert mock_update.call_args[0][1] == 123

    @patch('tags.routes.TagsService.update')
    def test_accepts_timestamp_update(self, mock_update, sample_tag):
        mock_update.return_value = sample_tag
        response = client.put("/tags/1/100", json={"tag": "updated", "timestamp": 9999999999})
        assert response.status_code == 200


class TestDeleteTag:
    @patch('tags.routes.TagsService.delete')
    def test_returns_204_when_deleted(self, mock_delete):
        mock_delete.return_value = True
        response = client.delete("/tags/1/100")
        assert response.status_code == 204

    @patch('tags.routes.TagsService.delete')
    def test_returns_404_when_not_found(self, mock_delete):
        mock_delete.return_value = False
        response = client.delete("/tags/999/999")
        assert response.status_code == 404

    @patch('tags.routes.TagsService.delete')
    def test_calls_service_with_correct_ids(self, mock_delete):
        mock_delete.return_value = True
        client.delete("/tags/42/123")
        mock_delete.assert_called_once_with(42, 123)

    @patch('tags.routes.TagsService.delete')
    def test_returns_no_content(self, mock_delete):
        mock_delete.return_value = True
        response = client.delete("/tags/1/100")
        assert response.content == b''

    @patch('tags.routes.TagsService.delete')
    def test_returns_error_detail_when_not_found(self, mock_delete):
        mock_delete.return_value = False
        response = client.delete("/tags/999/999")
        assert "detail" in response.json()

