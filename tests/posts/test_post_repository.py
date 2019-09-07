from unittest.mock import Mock, patch
from apps.posts.models import Post


@patch('core.databases.session')
def test_get_post(session):
    post = session.query(Post).filter(Post.id == 1).first.return_value = 1
    print(session.query(Post).filter(Post.id == 1).first())
