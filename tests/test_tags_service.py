import pytest
from unittest.mock import Mock, patch
from tags.service import TagsService
from tags.models.db_table import TagORM
from tags.models.response import Tag
from tags.models.request import TagCreate, TagUpdate


@pytest.fixture
def mock_session():
    session = Mock()
    session.__enter__ = Mock(return_value=session)
    session.__exit__ = Mock(return_value=False)
    return session


@pytest.fixture
def sample_tag_orm():
    return TagORM(id=1, userId=1, movieId=100, tag="great movie", timestamp=1234567890)


@pytest.fixture
def sample_tag_orm_list():
    return [
        TagORM(id=1, userId=1, movieId=100, tag="great movie", timestamp=1234567890),
        TagORM(id=2, userId=2, movieId=101, tag="awesome", timestamp=1234567891)
    ]


class TestGetAll:
    @patch('tags.service.get_session')
    def test_returns_list(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = []
        result = TagsService.get_all()
        assert isinstance(result, list)

    @patch('tags.service.get_session')
    def test_returns_tag_models(self, mock_get_session, mock_session, sample_tag_orm_list):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = sample_tag_orm_list
        result = TagsService.get_all()
        assert all(isinstance(t, Tag) for t in result)

    @patch('tags.service.get_session')
    def test_queries_tag_orm(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = []
        TagsService.get_all()
        mock_session.query.assert_called_once_with(TagORM)

    @patch('tags.service.get_session')
    def test_returns_correct_count(self, mock_get_session, mock_session, sample_tag_orm_list):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = sample_tag_orm_list
        result = TagsService.get_all()
        assert len(result) == 2

    @patch('tags.service.get_session')
    def test_returns_empty_list_when_no_tags(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.all.return_value = []
        result = TagsService.get_all()
        assert result == []


class TestGetByUserAndMovie:
    @patch('tags.service.get_session')
    def test_returns_tag_when_found(self, mock_get_session, mock_session, sample_tag_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_tag_orm
        result = TagsService.get_by_user_and_movie(1, 100)
        assert isinstance(result, Tag)

    @patch('tags.service.get_session')
    def test_returns_none_when_not_found(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        result = TagsService.get_by_user_and_movie(999, 999)
        assert result is None

    @patch('tags.service.get_session')
    def test_filters_by_user_and_movie(self, mock_get_session, mock_session, sample_tag_orm):
        mock_get_session.return_value = mock_session
        mock_query = mock_session.query.return_value
        mock_query.filter.return_value.first.return_value = sample_tag_orm
        TagsService.get_by_user_and_movie(1, 100)
        mock_query.filter.assert_called_once()

    @patch('tags.service.get_session')
    def test_returns_correct_tag_data(self, mock_get_session, mock_session, sample_tag_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_tag_orm
        result = TagsService.get_by_user_and_movie(1, 100)
        assert result.tag == "great movie"

    @patch('tags.service.get_session')
    def test_returns_tag_with_timestamp(self, mock_get_session, mock_session, sample_tag_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_tag_orm
        result = TagsService.get_by_user_and_movie(1, 100)
        assert result.timestamp == 1234567890


class TestCreate:
    @patch('tags.service.get_session')
    def test_returns_tag_model(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.add.return_value = None

        def refresh_side_effect(obj):
            obj.id = 1
            obj.userId = 1
            obj.movieId = 100
            obj.tag = "great movie"
            obj.timestamp = 1234567890

        mock_session.refresh.side_effect = refresh_side_effect
        tag_data = TagCreate(userId=1, movieId=100, tag="great movie", timestamp=1234567890)
        result = TagsService.create(tag_data)
        assert isinstance(result, Tag)

    @patch('tags.service.get_session')
    def test_adds_to_session(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session

        def refresh_side_effect(obj):
            obj.id = 1
            obj.userId = 1
            obj.movieId = 100
            obj.tag = "great movie"
            obj.timestamp = 1234567890

        mock_session.refresh.side_effect = refresh_side_effect
        tag_data = TagCreate(userId=1, movieId=100, tag="great movie", timestamp=1234567890)
        TagsService.create(tag_data)
        mock_session.add.assert_called_once()

    @patch('tags.service.get_session')
    def test_commits_transaction(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session

        def refresh_side_effect(obj):
            obj.id = 1
            obj.userId = 1
            obj.movieId = 100
            obj.tag = "great movie"
            obj.timestamp = 1234567890

        mock_session.refresh.side_effect = refresh_side_effect
        tag_data = TagCreate(userId=1, movieId=100, tag="great movie", timestamp=1234567890)
        TagsService.create(tag_data)
        mock_session.commit.assert_called_once()

    @patch('tags.service.get_session')
    def test_refreshes_object(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session

        def refresh_side_effect(obj):
            obj.id = 1
            obj.userId = 1
            obj.movieId = 100
            obj.tag = "great movie"
            obj.timestamp = 1234567890

        mock_session.refresh.side_effect = refresh_side_effect
        tag_data = TagCreate(userId=1, movieId=100, tag="great movie", timestamp=1234567890)
        TagsService.create(tag_data)
        mock_session.refresh.assert_called_once()

    @patch('tags.service.get_session')
    def test_creates_with_correct_data(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session

        def refresh_side_effect(obj):
            obj.id = 1
            obj.userId = 1
            obj.movieId = 100
            obj.tag = "great movie"
            obj.timestamp = 1234567890

        mock_session.refresh.side_effect = refresh_side_effect
        tag_data = TagCreate(userId=1, movieId=100, tag="great movie", timestamp=1234567890)
        result = TagsService.create(tag_data)
        assert result.tag == "great movie" and result.userId == 1


class TestUpdate:
    @patch('tags.service.get_session')
    def test_returns_updated_tag(self, mock_get_session, mock_session, sample_tag_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_tag_orm
        tag_data = TagUpdate(tag="updated tag")
        result = TagsService.update(1, 100, tag_data)
        assert isinstance(result, Tag)

    @patch('tags.service.get_session')
    def test_returns_none_when_not_found(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        tag_data = TagUpdate(tag="updated tag")
        result = TagsService.update(999, 999, tag_data)
        assert result is None

    @patch('tags.service.get_session')
    def test_commits_changes(self, mock_get_session, mock_session, sample_tag_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_tag_orm
        tag_data = TagUpdate(tag="updated tag")
        TagsService.update(1, 100, tag_data)
        mock_session.commit.assert_called_once()

    @patch('tags.service.get_session')
    def test_updates_tag_value(self, mock_get_session, mock_session, sample_tag_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_tag_orm
        tag_data = TagUpdate(tag="updated tag")
        TagsService.update(1, 100, tag_data)
        assert sample_tag_orm.tag == "updated tag"

    @patch('tags.service.get_session')
    def test_updates_timestamp_when_provided(self, mock_get_session, mock_session, sample_tag_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_tag_orm
        tag_data = TagUpdate(tag="updated tag", timestamp=9999999999)
        TagsService.update(1, 100, tag_data)
        assert sample_tag_orm.timestamp == 9999999999


class TestDelete:
    @patch('tags.service.get_session')
    def test_returns_true_when_deleted(self, mock_get_session, mock_session, sample_tag_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_tag_orm
        result = TagsService.delete(1, 100)
        assert result is True

    @patch('tags.service.get_session')
    def test_returns_false_when_not_found(self, mock_get_session, mock_session):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        result = TagsService.delete(999, 999)
        assert result is False

    @patch('tags.service.get_session')
    def test_calls_delete_on_session(self, mock_get_session, mock_session, sample_tag_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_tag_orm
        TagsService.delete(1, 100)
        mock_session.delete.assert_called_once_with(sample_tag_orm)

    @patch('tags.service.get_session')
    def test_commits_deletion(self, mock_get_session, mock_session, sample_tag_orm):
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_tag_orm
        TagsService.delete(1, 100)
        mock_session.commit.assert_called_once()

    @patch('tags.service.get_session')
    def test_queries_correct_tag(self, mock_get_session, mock_session, sample_tag_orm):
        mock_get_session.return_value = mock_session
        mock_query = mock_session.query.return_value
        mock_query.filter.return_value.first.return_value = sample_tag_orm
        TagsService.delete(1, 100)
        mock_query.filter.assert_called_once()

