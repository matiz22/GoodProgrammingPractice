import pytest
from unittest.mock import Mock, patch
from links.service import LinksService
from links.models.db_table import LinkORM
from links.models.response import Link
from links.models.request import LinkCreate, LinkUpdate


@pytest.fixture
def mock_session():
    session = Mock()
    session.__enter__ = Mock(return_value=session)
    session.__exit__ = Mock(return_value=False)
    return session


@pytest.fixture
def sample_link_orm():
    return LinkORM(movieId=1, imdbId=12345, tmdbId=67890)


@pytest.fixture
def sample_link_orm_list():
    return [
        LinkORM(movieId=1, imdbId=12345, tmdbId=67890),
        LinkORM(movieId=2, imdbId=54321, tmdbId=98765)
    ]


class TestGetAll:
    @patch('links.service.get_session')
    def test_returns_list(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = []
        result = LinksService.get_all()
        assert isinstance(result, list)

    @patch('links.service.get_session')
    def test_returns_link_models(self, mock_get_session, mock_session, sample_link_orm_list):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = sample_link_orm_list
        result = LinksService.get_all()
        assert all(isinstance(link, Link) for link in result)

    @patch('links.service.get_session')
    def test_queries_link_orm(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = []
        LinksService.get_all()
        mock_session.query.assert_called_once_with(LinkORM)

    @patch('links.service.get_session')
    def test_returns_correct_count(self, mock_get_session, mock_session, sample_link_orm_list):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = sample_link_orm_list
        result = LinksService.get_all()
        assert len(result) == 2

    @patch('links.service.get_session')
    def test_returns_empty_list_when_no_links(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = []
        result = LinksService.get_all()
        assert result == []


class TestGetById:
    @patch('links.service.get_session')
    def test_returns_link_when_found(self, mock_get_session, mock_session, sample_link_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_link_orm
        result = LinksService.get_by_id(1)
        assert isinstance(result, Link)

    @patch('links.service.get_session')
    def test_returns_none_when_not_found(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        result = LinksService.get_by_id(999)
        assert result is None

    @patch('links.service.get_session')
    def test_filters_by_correct_movie_id(self, mock_get_session, mock_session, sample_link_orm):
        mock_get_session.return_value = mock_session
        mock_query = mock_session.query.return_value
        mock_query.filter.return_value.first.return_value = sample_link_orm
        LinksService.get_by_id(42)
        mock_query.filter.assert_called_once()

    @patch('links.service.get_session')
    def test_returns_correct_link_data(self, mock_get_session, mock_session, sample_link_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_link_orm
        result = LinksService.get_by_id(1)
        assert result.movieId == 1

    @patch('links.service.get_session')
    def test_returns_link_with_imdb_and_tmdb(self, mock_get_session, mock_session, sample_link_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_link_orm
        result = LinksService.get_by_id(1)
        assert result.imdbId == 12345 and result.tmdbId == 67890


class TestCreate:
    @patch('links.service.get_session')
    def test_returns_link_model(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.add.return_value = None

        def refresh_side_effect(obj):
            obj.movieId = 1
            obj.imdbId = 12345
            obj.tmdbId = 67890

        mock_session.refresh.side_effect = refresh_side_effect
        link_data = LinkCreate(movieId=1, imdbId="12345", tmdbId="67890")
        result = LinksService.create(link_data)
        assert isinstance(result, Link)

    @patch('links.service.get_session')
    def test_adds_to_session(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session

        def refresh_side_effect(obj):
            obj.movieId = 1
            obj.imdbId = 12345
            obj.tmdbId = 67890

        mock_session.refresh.side_effect = refresh_side_effect
        link_data = LinkCreate(movieId=1, imdbId="12345", tmdbId="67890")
        LinksService.create(link_data)
        mock_session.add.assert_called_once()

    @patch('links.service.get_session')
    def test_commits_transaction(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session

        def refresh_side_effect(obj):
            obj.movieId = 1
            obj.imdbId = 12345
            obj.tmdbId = 67890

        mock_session.refresh.side_effect = refresh_side_effect
        link_data = LinkCreate(movieId=1, imdbId="12345", tmdbId="67890")
        LinksService.create(link_data)
        mock_session.commit.assert_called_once()

    @patch('links.service.get_session')
    def test_refreshes_object(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session

        def refresh_side_effect(obj):
            obj.movieId = 1
            obj.imdbId = 12345
            obj.tmdbId = 67890

        mock_session.refresh.side_effect = refresh_side_effect
        link_data = LinkCreate(movieId=1, imdbId="12345", tmdbId="67890")
        LinksService.create(link_data)
        mock_session.refresh.assert_called_once()

    @patch('links.service.get_session')
    def test_creates_with_correct_data(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session

        def refresh_side_effect(obj):
            obj.movieId = 1
            obj.imdbId = 12345
            obj.tmdbId = 67890

        mock_session.refresh.side_effect = refresh_side_effect
        link_data = LinkCreate(movieId=1, imdbId="12345", tmdbId="67890")
        result = LinksService.create(link_data)
        assert result.movieId == 1 and result.imdbId == 12345


class TestUpdate:
    @patch('links.service.get_session')
    def test_returns_updated_link(self, mock_get_session, mock_session, sample_link_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_link_orm
        link_data = LinkUpdate(imdbId="99999")
        result = LinksService.update(1, link_data)
        assert isinstance(result, Link)

    @patch('links.service.get_session')
    def test_returns_none_when_not_found(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        link_data = LinkUpdate(imdbId="99999")
        result = LinksService.update(999, link_data)
        assert result is None

    @patch('links.service.get_session')
    def test_commits_changes(self, mock_get_session, mock_session, sample_link_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_link_orm
        link_data = LinkUpdate(imdbId="99999")
        LinksService.update(1, link_data)
        mock_session.commit.assert_called_once()

    @patch('links.service.get_session')
    def test_updates_correct_attributes(self, mock_get_session, mock_session, sample_link_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_link_orm
        link_data = LinkUpdate(imdbId="99999")
        LinksService.update(1, link_data)
        assert sample_link_orm.imdbId == "99999"

    @patch('links.service.get_session')
    def test_ignores_none_values(self, mock_get_session, mock_session, sample_link_orm):
        mock_get_session.return_value = mock_session
        original_tmdb = sample_link_orm.tmdbId
        mock_session.query.return_value.filter.return_value.first.return_value = sample_link_orm
        link_data = LinkUpdate(imdbId="99999", tmdbId=None)
        LinksService.update(1, link_data)
        assert sample_link_orm.tmdbId == original_tmdb


class TestDelete:
    @patch('links.service.get_session')
    def test_returns_true_when_deleted(self, mock_get_session, mock_session, sample_link_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_link_orm
        result = LinksService.delete(1)
        assert result is True

    @patch('links.service.get_session')
    def test_returns_false_when_not_found(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        result = LinksService.delete(999)
        assert result is False

    @patch('links.service.get_session')
    def test_calls_delete_on_session(self, mock_get_session, mock_session, sample_link_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_link_orm
        LinksService.delete(1)
        mock_session.delete.assert_called_once_with(sample_link_orm)

    @patch('links.service.get_session')
    def test_commits_deletion(self, mock_get_session, mock_session, sample_link_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_link_orm
        LinksService.delete(1)
        mock_session.commit.assert_called_once()

    @patch('links.service.get_session')
    def test_queries_correct_link(self, mock_get_session, mock_session, sample_link_orm):
        mock_get_session.return_value = mock_session
        mock_query = mock_session.query.return_value
        mock_query.filter.return_value.first.return_value = sample_link_orm
        LinksService.delete(42)
        mock_query.filter.assert_called_once()

