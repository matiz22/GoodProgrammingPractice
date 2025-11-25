import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from links.models.response import Link


client = TestClient(app)


@pytest.fixture
def sample_link():
    return Link(movieId=1, imdbId=12345, tmdbId=67890)


@pytest.fixture
def sample_links_list():
    return [
        Link(movieId=1, imdbId=12345, tmdbId=67890),
        Link(movieId=2, imdbId=54321, tmdbId=98765)
    ]


class TestGetLinks:
    @patch('links.routes.LinksService.get_all')
    def test_returns_200_status(self, mock_get_all, sample_links_list):
        mock_get_all.return_value = sample_links_list
        response = client.get("/links/")
        assert response.status_code == 200

    @patch('links.routes.LinksService.get_all')
    def test_returns_list_of_links(self, mock_get_all, sample_links_list):
        mock_get_all.return_value = sample_links_list
        response = client.get("/links/")
        assert isinstance(response.json(), list)

    @patch('links.routes.LinksService.get_all')
    def test_returns_correct_count(self, mock_get_all, sample_links_list):
        mock_get_all.return_value = sample_links_list
        response = client.get("/links/")
        assert len(response.json()) == 2

    @patch('links.routes.LinksService.get_all')
    def test_returns_empty_list(self, mock_get_all):
        mock_get_all.return_value = []
        response = client.get("/links/")
        assert response.json() == []

    @patch('links.routes.LinksService.get_all')
    def test_calls_service_method(self, mock_get_all, sample_links_list):
        mock_get_all.return_value = sample_links_list
        client.get("/links/")
        mock_get_all.assert_called_once()


class TestGetLink:
    @patch('links.routes.LinksService.get_by_id')
    def test_returns_200_when_found(self, mock_get_by_id, sample_link):
        mock_get_by_id.return_value = sample_link
        response = client.get("/links/1")
        assert response.status_code == 200

    @patch('links.routes.LinksService.get_by_id')
    def test_returns_404_when_not_found(self, mock_get_by_id):
        mock_get_by_id.return_value = None
        response = client.get("/links/999")
        assert response.status_code == 404

    @patch('links.routes.LinksService.get_by_id')
    def test_returns_link_data(self, mock_get_by_id, sample_link):
        mock_get_by_id.return_value = sample_link
        response = client.get("/links/1")
        assert response.json()["movieId"] == 1

    @patch('links.routes.LinksService.get_by_id')
    def test_calls_service_with_correct_id(self, mock_get_by_id, sample_link):
        mock_get_by_id.return_value = sample_link
        client.get("/links/42")
        mock_get_by_id.assert_called_once_with(42)

    @patch('links.routes.LinksService.get_by_id')
    def test_returns_error_detail(self, mock_get_by_id):
        mock_get_by_id.return_value = None
        response = client.get("/links/999")
        assert "detail" in response.json()


class TestCreateLink:
    @patch('links.routes.LinksService.create')
    def test_returns_201_status(self, mock_create, sample_link):
        mock_create.return_value = sample_link
        response = client.post("/links/", json={"movieId": 1, "imdbId": "12345", "tmdbId": "67890"})
        assert response.status_code == 201

    @patch('links.routes.LinksService.create')
    def test_returns_created_link(self, mock_create, sample_link):
        mock_create.return_value = sample_link
        response = client.post("/links/", json={"movieId": 1, "imdbId": "12345", "tmdbId": "67890"})
        assert response.json()["movieId"] == 1

    @patch('links.routes.LinksService.create')
    def test_calls_service_with_data(self, mock_create, sample_link):
        mock_create.return_value = sample_link
        client.post("/links/", json={"movieId": 1, "imdbId": "12345", "tmdbId": "67890"})
        mock_create.assert_called_once()

    @patch('links.routes.LinksService.create')
    def test_validates_request_body(self, mock_create):
        response = client.post("/links/", json={})
        assert response.status_code == 422

    @patch('links.routes.LinksService.create')
    def test_returns_link_with_all_fields(self, mock_create, sample_link):
        mock_create.return_value = sample_link
        response = client.post("/links/", json={"movieId": 1, "imdbId": "12345", "tmdbId": "67890"})
        data = response.json()
        assert all(key in data for key in ["movieId", "imdbId", "tmdbId"])


class TestUpdateLink:
    @patch('links.routes.LinksService.update')
    def test_returns_200_when_updated(self, mock_update, sample_link):
        mock_update.return_value = sample_link
        response = client.put("/links/1", json={"imdbId": "99999"})
        assert response.status_code == 200

    @patch('links.routes.LinksService.update')
    def test_returns_404_when_not_found(self, mock_update):
        mock_update.return_value = None
        response = client.put("/links/999", json={"imdbId": "99999"})
        assert response.status_code == 404

    @patch('links.routes.LinksService.update')
    def test_returns_updated_link(self, mock_update, sample_link):
        mock_update.return_value = sample_link
        response = client.put("/links/1", json={"imdbId": "99999"})
        assert "movieId" in response.json()

    @patch('links.routes.LinksService.update')
    def test_calls_service_with_id_and_data(self, mock_update, sample_link):
        mock_update.return_value = sample_link
        client.put("/links/42", json={"imdbId": "99999"})
        assert mock_update.call_args[0][0] == 42

    @patch('links.routes.LinksService.update')
    def test_accepts_partial_updates(self, mock_update, sample_link):
        mock_update.return_value = sample_link
        response = client.put("/links/1", json={"imdbId": "99999"})
        assert response.status_code == 200


class TestDeleteLink:
    @patch('links.routes.LinksService.delete')
    def test_returns_204_when_deleted(self, mock_delete):
        mock_delete.return_value = True
        response = client.delete("/links/1")
        assert response.status_code == 204

    @patch('links.routes.LinksService.delete')
    def test_returns_404_when_not_found(self, mock_delete):
        mock_delete.return_value = False
        response = client.delete("/links/999")
        assert response.status_code == 404

    @patch('links.routes.LinksService.delete')
    def test_calls_service_with_correct_id(self, mock_delete):
        mock_delete.return_value = True
        client.delete("/links/42")
        mock_delete.assert_called_once_with(42)

    @patch('links.routes.LinksService.delete')
    def test_returns_no_content(self, mock_delete):
        mock_delete.return_value = True
        response = client.delete("/links/1")
        assert response.content == b''

    @patch('links.routes.LinksService.delete')
    def test_returns_error_detail_when_not_found(self, mock_delete):
        mock_delete.return_value = False
        response = client.delete("/links/999")
        assert "detail" in response.json()

