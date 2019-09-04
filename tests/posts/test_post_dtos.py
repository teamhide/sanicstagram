from apps.posts.dtos import (CreatePostDto, FeedViewPostDto, CreateCommentDto,
                             DeleteCommentDto, LikePostDto, UnLikePostDto,
                             GetPostLikedUsersDto, SearchTagDto, DeletePostDto,
                             GetPostDto, UpdatePostDto)


def test_create_post_dto(app):
    dto = CreatePostDto(
        user_id=1,
        attachments=[],
        caption='first caption'
    )


def test_feed_view_post_dto(app):
    dto = FeedViewPostDto()


def test_create_comment_dto(app):
    dto = CreateCommentDto()


def test_delete_comment_dto(app):
    dto = DeleteCommentDto()


def test_like_post_dto(app):
    dto = LikePostDto()


def test_unlike_post_dto(app):
    dto = UnLikePostDto()


def test_get_post_liked_user_dto(app):
    dto = GetPostLikedUsersDto()


def test_search_tag_dto(app):
    dto = SearchTagDto()


def test_delete_post_dto(app):
    dto = DeletePostDto()


def test_get_post_dto(app):
    dto = GetPostDto()


def test_update_post_dto(app):
    dto = UpdatePostDto()
