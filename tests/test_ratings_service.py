import pytest
from unittest.mock import Mock, patch
from ratings.service import RatingsService
from ratings.models.db_table import RatingORM
from ratings.models.response import Rating
from ratings.models.request import RatingCreate, RatingUpdate


@pytest.fixture
def mock_session():
    session = Mock()
    session.__enter__ = Mock(return_value=session)
    session.__exit__ = Mock(return_value=False)
    return session


@pytest.fixture
def sample_rating_orm():
    return RatingORM(userId=1, movieId=100, rating=4.5, timestamp=1234567890)


@pytest.fixture
def sample_rating_orm_list():
    return [
        RatingORM(userId=1, movieId=100, rating=4.5, timestamp=1234567890),
        RatingORM(userId=2, movieId=101, rating=3.5, timestamp=1234567891)
    ]


class TestGetAll:
    @patch('ratings.service.get_session')
    def test_returns_list(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = []
        result = RatingsService.get_all()
        assert isinstance(result, list)

    @patch('ratings.service.get_session')
    def test_returns_rating_models(self, mock_get_session, mock_session, sample_rating_orm_list):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = sample_rating_orm_list
        result = RatingsService.get_all()
        assert all(isinstance(r, Rating) for r in result)

    @patch('ratings.service.get_session')
    def test_queries_rating_orm(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = []
        RatingsService.get_all()
        mock_session.query.assert_called_once_with(RatingORM)

    @patch('ratings.service.get_session')
    def test_returns_correct_count(self, mock_get_session, mock_session, sample_rating_orm_list):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = sample_rating_orm_list
        result = RatingsService.get_all()
        assert len(result) == 2

    @patch('ratings.service.get_session')
    def test_returns_empty_list_when_no_ratings(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = []
        result = RatingsService.get_all()
        assert result == []


class TestGetByUserAndMovie:
    @patch('ratings.service.get_session')
    def test_returns_rating_when_found(self, mock_get_session, mock_session, sample_rating_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_rating_orm
        result = RatingsService.get_by_user_and_movie(1, 100)
        assert isinstance(result, Rating)

    @patch('ratings.service.get_session')
    def test_returns_none_when_not_found(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        result = RatingsService.get_by_user_and_movie(999, 999)
        assert result is None

    @patch('ratings.service.get_session')
    def test_filters_by_user_and_movie(self, mock_get_session, mock_session, sample_rating_orm):
        mock_get_session.return_value = mock_session
        mock_query = mock_session.query.return_value
        mock_query.filter.return_value.first.return_value = sample_rating_orm
        RatingsService.get_by_user_and_movie(1, 100)
        mock_query.filter.assert_called_once()

    @patch('ratings.service.get_session')
    def test_returns_correct_rating_data(self, mock_get_session, mock_session, sample_rating_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_rating_orm
        result = RatingsService.get_by_user_and_movie(1, 100)
        assert result.rating == 4.5

    @patch('ratings.service.get_session')
    def test_returns_rating_with_timestamp(self, mock_get_session, mock_session, sample_rating_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_rating_orm
        result = RatingsService.get_by_user_and_movie(1, 100)
        assert result.timestamp == 1234567890


class TestCreate:
    @patch('ratings.service.get_session')
    def test_returns_rating_model(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.add.return_value = None

        def refresh_side_effect(obj):
            obj.userId = 1
            obj.movieId = 100
            obj.rating = 4.5
            obj.timestamp = 1234567890

        mock_session.refresh.side_effect = refresh_side_effect
        rating_data = RatingCreate(userId=1, movieId=100, rating=4.5, timestamp=1234567890)
        result = RatingsService.create(rating_data)
        assert isinstance(result, Rating)

    @patch('ratings.service.get_session')
    def test_adds_to_session(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session

        def refresh_side_effect(obj):
            obj.userId = 1
            obj.movieId = 100
            obj.rating = 4.5
            obj.timestamp = 1234567890

        mock_session.refresh.side_effect = refresh_side_effect
        rating_data = RatingCreate(userId=1, movieId=100, rating=4.5, timestamp=1234567890)
        RatingsService.create(rating_data)
        mock_session.add.assert_called_once()

    @patch('ratings.service.get_session')
    def test_commits_transaction(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session

        def refresh_side_effect(obj):
            obj.userId = 1
            obj.movieId = 100
            obj.rating = 4.5
            obj.timestamp = 1234567890

        mock_session.refresh.side_effect = refresh_side_effect
        rating_data = RatingCreate(userId=1, movieId=100, rating=4.5, timestamp=1234567890)
        RatingsService.create(rating_data)
        mock_session.commit.assert_called_once()

    @patch('ratings.service.get_session')
    def test_refreshes_object(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session

        def refresh_side_effect(obj):
            obj.userId = 1
            obj.movieId = 100
            obj.rating = 4.5
            obj.timestamp = 1234567890

        mock_session.refresh.side_effect = refresh_side_effect
        rating_data = RatingCreate(userId=1, movieId=100, rating=4.5, timestamp=1234567890)
        RatingsService.create(rating_data)
        mock_session.refresh.assert_called_once()

    @patch('ratings.service.get_session')
    def test_creates_with_correct_data(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session

        def refresh_side_effect(obj):
            obj.userId = 1
            obj.movieId = 100
            obj.rating = 4.5
            obj.timestamp = 1234567890

        mock_session.refresh.side_effect = refresh_side_effect
        rating_data = RatingCreate(userId=1, movieId=100, rating=4.5, timestamp=1234567890)
        result = RatingsService.create(rating_data)
        assert result.rating == 4.5 and result.userId == 1


class TestUpdate:
    @patch('ratings.service.get_session')
    def test_returns_updated_rating(self, mock_get_session, mock_session, sample_rating_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_rating_orm
        rating_data = RatingUpdate(rating=5.0)
        result = RatingsService.update(1, 100, rating_data)
        assert isinstance(result, Rating)

    @patch('ratings.service.get_session')
    def test_returns_none_when_not_found(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        rating_data = RatingUpdate(rating=5.0)
        result = RatingsService.update(999, 999, rating_data)
        assert result is None

    @patch('ratings.service.get_session')
    def test_commits_changes(self, mock_get_session, mock_session, sample_rating_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_rating_orm
        rating_data = RatingUpdate(rating=5.0)
        RatingsService.update(1, 100, rating_data)
        mock_session.commit.assert_called_once()

    @patch('ratings.service.get_session')
    def test_updates_rating_value(self, mock_get_session, mock_session, sample_rating_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_rating_orm
        rating_data = RatingUpdate(rating=5.0)
        RatingsService.update(1, 100, rating_data)
        assert sample_rating_orm.rating == 5.0

    @patch('ratings.service.get_session')
    def test_updates_timestamp_when_provided(self, mock_get_session, mock_session, sample_rating_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_rating_orm
        rating_data = RatingUpdate(rating=5.0, timestamp=9999999999)
        RatingsService.update(1, 100, rating_data)
        assert sample_rating_orm.timestamp == 9999999999


class TestDelete:
    @patch('ratings.service.get_session')
    def test_returns_true_when_deleted(self, mock_get_session, mock_session, sample_rating_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_rating_orm
        result = RatingsService.delete(1, 100)
        assert result is True

    @patch('ratings.service.get_session')
    def test_returns_false_when_not_found(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        result = RatingsService.delete(999, 999)
        assert result is False

    @patch('ratings.service.get_session')
    def test_calls_delete_on_session(self, mock_get_session, mock_session, sample_rating_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_rating_orm
        RatingsService.delete(1, 100)
        mock_session.delete.assert_called_once_with(sample_rating_orm)

    @patch('ratings.service.get_session')
    def test_commits_deletion(self, mock_get_session, mock_session, sample_rating_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_rating_orm
        RatingsService.delete(1, 100)
        mock_session.commit.assert_called_once()

    @patch('ratings.service.get_session')
    def test_queries_correct_rating(self, mock_get_session, mock_session, sample_rating_orm):
        mock_get_session.return_value = mock_session
        mock_query = mock_session.query.return_value
        mock_query.filter.return_value.first.return_value = sample_rating_orm
        RatingsService.delete(1, 100)
        mock_query.filter.assert_called_once()

