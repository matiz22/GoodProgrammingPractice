import pytest
from unittest.mock import Mock, patch, MagicMock
from movies.service import MoviesService
from movies.models.db_table import MovieORM
from movies.models.response import Movie


@pytest.fixture
def mock_session():
    session = Mock()
    session.__enter__ = Mock(return_value=session)
    session.__exit__ = Mock(return_value=False)
    return session


@pytest.fixture
def sample_movie_orm():
    return MovieORM(movieId=1, title="Test Movie", genres=["Action", "Drama"])


@pytest.fixture
def sample_movie_orm_list():
    return [
        MovieORM(movieId=1, title="Test Movie", genres=["Action", "Drama"]),
        MovieORM(movieId=2, title="Another Movie", genres=["Comedy"])
    ]


class TestGetAll:
    @patch('movies.service.get_session')
    def test_returns_list(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = []
        result = MoviesService.get_all()
        assert isinstance(result, list)

    @patch('movies.service.get_session')
    def test_returns_movie_models(self, mock_get_session, mock_session, sample_movie_orm_list):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = sample_movie_orm_list
        result = MoviesService.get_all()
        assert all(isinstance(m, Movie) for m in result)

    @patch('movies.service.get_session')
    def test_queries_movie_orm(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = []
        MoviesService.get_all()
        mock_session.query.assert_called_once_with(MovieORM)

    @patch('movies.service.get_session')
    def test_returns_correct_count(self, mock_get_session, mock_session, sample_movie_orm_list):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = sample_movie_orm_list
        result = MoviesService.get_all()
        assert len(result) == 2

    @patch('movies.service.get_session')
    def test_returns_empty_list_when_no_movies(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = []
        result = MoviesService.get_all()
        assert result == []


class TestGetById:
    @patch('movies.service.get_session')
    def test_returns_movie_when_found(self, mock_get_session, mock_session, sample_movie_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_movie_orm
        result = MoviesService.get_by_id(1)
        assert isinstance(result, Movie)

    @patch('movies.service.get_session')
    def test_returns_none_when_not_found(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        result = MoviesService.get_by_id(999)
        assert result is None

    @patch('movies.service.get_session')
    def test_filters_by_correct_id(self, mock_get_session, mock_session, sample_movie_orm):
        mock_get_session.return_value = mock_session
        mock_query = mock_session.query.return_value
        mock_query.filter.return_value.first.return_value = sample_movie_orm
        MoviesService.get_by_id(42)
        mock_query.filter.assert_called_once()

    @patch('movies.service.get_session')
    def test_returns_correct_movie_data(self, mock_get_session, mock_session, sample_movie_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_movie_orm
        result = MoviesService.get_by_id(1)
        assert result.title == "Test Movie"

    @patch('movies.service.get_session')
    def test_returns_movie_with_genres(self, mock_get_session, mock_session, sample_movie_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_movie_orm
        result = MoviesService.get_by_id(1)
        assert result.genres == ["Action", "Drama"]


class TestCreate:
    @patch('movies.service.get_session')
    def test_returns_movie_model(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.add.return_value = None

        def refresh_side_effect(obj):
            obj.movieId = 1
            obj.title = "New Movie"
            obj.genres = ["Action"]

        mock_session.refresh.side_effect = refresh_side_effect
        result = MoviesService.create({"title": "New Movie", "genres": ["Action"]})
        assert isinstance(result, Movie)

    @patch('movies.service.get_session')
    def test_adds_to_session(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session

        def refresh_side_effect(obj):
            obj.movieId = 1
            obj.title = "New Movie"
            obj.genres = ["Action"]

        mock_session.refresh.side_effect = refresh_side_effect
        MoviesService.create({"title": "New Movie", "genres": ["Action"]})
        mock_session.add.assert_called_once()

    @patch('movies.service.get_session')
    def test_commits_transaction(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session

        def refresh_side_effect(obj):
            obj.movieId = 1
            obj.title = "New Movie"
            obj.genres = ["Action"]

        mock_session.refresh.side_effect = refresh_side_effect
        MoviesService.create({"title": "New Movie", "genres": ["Action"]})
        mock_session.commit.assert_called_once()

    @patch('movies.service.get_session')
    def test_refreshes_object(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session

        def refresh_side_effect(obj):
            obj.movieId = 1
            obj.title = "New Movie"
            obj.genres = ["Action"]

        mock_session.refresh.side_effect = refresh_side_effect
        MoviesService.create({"title": "New Movie", "genres": ["Action"]})
        mock_session.refresh.assert_called_once()

    @patch('movies.service.get_session')
    def test_creates_with_correct_data(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session

        def refresh_side_effect(obj):
            obj.movieId = 1

        mock_session.refresh.side_effect = refresh_side_effect
        data = {"title": "New Movie", "genres": ["Action", "Drama"]}
        result = MoviesService.create(data)
        assert result.title == "New Movie"


class TestUpdate:
    @patch('movies.service.get_session')
    def test_returns_updated_movie(self, mock_get_session, mock_session, sample_movie_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_movie_orm
        result = MoviesService.update(1, {"title": "Updated"})
        assert isinstance(result, Movie)

    @patch('movies.service.get_session')
    def test_returns_none_when_not_found(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        result = MoviesService.update(999, {"title": "Updated"})
        assert result is None

    @patch('movies.service.get_session')
    def test_commits_changes(self, mock_get_session, mock_session, sample_movie_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_movie_orm
        MoviesService.update(1, {"title": "Updated"})
        mock_session.commit.assert_called_once()

    @patch('movies.service.get_session')
    def test_updates_correct_attributes(self, mock_get_session, mock_session, sample_movie_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_movie_orm
        MoviesService.update(1, {"title": "Updated Title"})
        assert sample_movie_orm.title == "Updated Title"

    @patch('movies.service.get_session')
    def test_ignores_none_values(self, mock_get_session, mock_session, sample_movie_orm):
        mock_get_session.return_value = mock_session
        original_genres = sample_movie_orm.genres
        mock_session.query.return_value.filter.return_value.first.return_value = sample_movie_orm
        MoviesService.update(1, {"title": "Updated", "genres": None})
        assert sample_movie_orm.genres == original_genres


class TestDelete:
    @patch('movies.service.get_session')
    def test_returns_true_when_deleted(self, mock_get_session, mock_session, sample_movie_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_movie_orm
        result = MoviesService.delete(1)
        assert result is True

    @patch('movies.service.get_session')
    def test_returns_false_when_not_found(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        result = MoviesService.delete(999)
        assert result is False

    @patch('movies.service.get_session')
    def test_calls_delete_on_session(self, mock_get_session, mock_session, sample_movie_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_movie_orm
        MoviesService.delete(1)
        mock_session.delete.assert_called_once_with(sample_movie_orm)

    @patch('movies.service.get_session')
    def test_commits_deletion(self, mock_get_session, mock_session, sample_movie_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_movie_orm
        MoviesService.delete(1)
        mock_session.commit.assert_called_once()

    @patch('movies.service.get_session')
    def test_queries_correct_movie(self, mock_get_session, mock_session, sample_movie_orm):
        mock_get_session.return_value = mock_session
        mock_query = mock_session.query.return_value
        mock_query.filter.return_value.first.return_value = sample_movie_orm
        MoviesService.delete(42)
        mock_query.filter.assert_called_once()
