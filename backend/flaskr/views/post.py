from sqlite3 import IntegrityError, Connection

import schema
from flask import g
from flask import request
from flask import Blueprint
from flask.views import MethodView
from werkzeug.exceptions import abort

from flaskr import settings
from flaskr.utils.auth import login_required
from flaskr.utils.db import get_db, get_all_posts, get_post, get_all_comments

bp_index = Blueprint("index", __name__, url_prefix='/api')
bp = Blueprint("post", __name__, url_prefix="/api/post")
bp_comment = Blueprint("comment", __name__, url_prefix='/api/comment')


class Index(MethodView):
    def get(self):
        """
        Get posts.
        :return json 200: List[Post]
        """
        return dict(posts=get_all_posts())


class Post(MethodView):
    def get(self):
        """
        Get posts.
        :return json 200: List[Post]
        """
        return dict(posts=get_all_posts())

    @staticmethod
    def post_schema(from_dict: dict) -> dict:
        try:
            data = schema.Schema({
                "title": schema.And(str, lambda x: settings.POST_TITLE_MIN_WORDS_LENGTH <= len(x) <= settings.POST_TITLE_MAX_WORDS_LENGTH),
                "body": schema.And(str, lambda x: settings.POST_BODY_MIN_WORDS_LENGTH <= len(x) <= settings.POST_BODY_MAX_WORDS_LENGTH)
            }).validate(from_dict)
        except schema.SchemaError:
            raise abort(400, "Wrong args.")
        else:
            return data

    @login_required
    def post(self):
        """
        Create a post
        :param form title: post title
        :param form body: post content text
        :return json 201: Post
        """
        data = self.post_schema(dict(request.form))

        db: Connection = get_db()

        try:
            with db:
                cur = db.cursor()
                cur.execute(
                    "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                    (data['title'], data['body'], g.user["id"]),
                )
        except IntegrityError:
            raise abort(400, "Duplicated data")

        post = get_post(post_id=cur.lastrowid)
        return dict(post), 201


class PostId(MethodView):
    def get(self, post_id: int):
        """
        Get post by specific id
        :param int post_id: id of post
        :return json 200: Post
        """
        post = get_post(post_id=post_id)

        if post is None:
            abort(404, f"Post id {post_id} doesn't exist.")

        return post


def comment_schema(form_dict: dict) -> dict:
    try:
        data = schema.Schema({
            "body": schema.And(
                str,
                lambda x: settings.COMMENT_BODY_MIN_WORDS_LENGTH <= len(x) <= settings.COMMENT_BODY_MAX_WORDS_LENGTH
            )
        }).validate(form_dict)
    except schema.SchemaError:
        raise abort(400, "Wrong args.")
    else:
        return data


class PostIdComment(MethodView):
    def get(self, post_id: int):
        """
        Get all comments of a post
        :param: int post_id:
        :return json 200: {"comments": List[Comment]}
        """
        return dict(comments=get_all_comments(post_id=post_id))

    @login_required
    def post(self, post_id: int):
        """
        Add a comment to post
        :param int post_id:
        :param form body:  comment content text
        :return json 201: Post
        """
        data = comment_schema(dict(request.form))
        db = get_db()
        with db:
            cur = db.cursor()
            cur.execute("INSERT INTO comment (author_id, body, parent_id, post_id) VALUES (?, ?, ?, ?)",
                        (g.user['id'], data['body'], None, post_id))

        return get_post(post_id), 201


class CommentId(MethodView):
    def get(self, comment_id: int):
        """
        Get a comment.
        :param int comment_id:
        :return json 200: Comment
        """
        row = get_db().execute("SELECT id, post_id, created, body FROM comment WHERE id=?", (comment_id, )).fetchone()
        if not row:
            raise abort(400, f'Comment {comment_id} not found.')
        return dict(row)


class CommentIdComment(MethodView):
    @login_required
    def post(self, comment_id: int):
        """
        Add a comment of a comment.
        Login required
        :param int comment_id: id of comment
        :param form body: comment content text
        :param form body: comment content text
        :raise 401 Login required:
        :return json 201: Post
        """
        data = comment_schema(dict(request.form))
        db = get_db()
        comment = db.execute(
            "SELECT post_id FROM comment WHERE id=?",
            (comment_id, )
        ).fetchone()
        if not comment:
            raise abort(400, f"Comment not found.")

        with db:
            cur = db.cursor()
            cur.execute("INSERT INTO comment (author_id, body, parent_id, post_id) VALUES (?, ?, ?, ?)",
                        (g.user['id'], data['body'], comment_id, comment['post_id']))

        return get_post(comment['post_id']), 201


bp_index.add_url_rule('/', view_func=Index.as_view('Index'))
bp.add_url_rule('/<int:post_id>/comment', view_func=PostIdComment.as_view('PostIdComment'))
bp.add_url_rule('/<int:post_id>', view_func=PostId.as_view('PostId'))
bp.add_url_rule('/', view_func=Post.as_view('Post'))

bp_comment.add_url_rule('/<int:comment_id>/comment',
                        view_func=CommentIdComment.as_view('PostIdCommentIdComment'))
bp_comment.add_url_rule('/<int:comment_id>', view_func=CommentId.as_view('PostIdCommentId'))
