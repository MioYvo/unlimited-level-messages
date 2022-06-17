"""
flaskr.utils.db
~~~~~~~~~~~~~~~
Utilities for database operations.
"""
import sqlite3
from typing import List, Optional
from datetime import datetime, timezone

from flask import g
from flask import current_app
from flaskr.utils.node import Node


def convert_timestamp(t):
    return datetime.fromisoformat(t.decode()).replace(tzinfo=timezone.utc).timestamp()


# Register the converter
sqlite3.register_converter("timestamp", convert_timestamp)


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """Clear existing data and create new tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql") as f:
            db.executescript(f.read().decode("utf8"))


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)


# modified from https://github.com/matthiask/django-tree-queries/blob/8863c5237f32585cc5ddc21041231155cb806149/tree_queries/compiler.py#L120
CTE = """WITH RECURSIVE __tree(tree_depth,
    tree_path,
    tree_ordering,
    tree_pk) AS (
    SELECT
        0 tree_depth,
        printf("%s ", id) tree_path,
        printf(" %020s ", id) tree_ordering,
        T.id tree_pk
    FROM comment T
    WHERE T.parent_id IS NULL
    UNION ALL
    SELECT
        __tree.tree_depth + 1,
        __tree.tree_path || printf("%s ", T.id),
        __tree.tree_ordering || printf("%020s ", T.id),
        T.id
    FROM comment T
    JOIN __tree ON T.parent_id = __tree.tree_pk
)
SELECT
    comment.id, 
    comment.parent_id, 
    comment.post_id,
    comment.body, comment.created, 
    comment.author_id, user.username as author_name,
-- __tree.tree_depth
   __tree.tree_path
FROM __tree 
JOIN comment ON comment.id=__tree.tree_pk
JOIN user ON user.id=comment.author_id
WHERE comment.post_id=?
-- AND instr(__tree.tree_path, '3') !=0
ORDER BY __tree.tree_ordering;
"""


def get_all_comments(post_id: int) -> List[Node]:
    root_nodes = Node.build_from_cte_rows(get_db().execute(CTE, (post_id, )))
    return list(root_nodes)


def put_in_child(parent: dict, child: dict):
    if 'children' in parent:
        parent['children'].append(child)
    else:
        parent['children'] = [child]


def get_post(post_id, with_comments=True) -> Optional[dict]:
    """Get a post and its author by id.

    :param post_id: id of post to get
    :param with_comments: if return with comments
    :return: the post with author information
    """
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (post_id,),
        )
        .fetchone()
    )

    if post is None:
        return None

    if with_comments:
        comments = get_all_comments(post_id=post['id'])
        return dict(post) | dict(comments=comments)
    else:
        return dict(post)


def get_all_posts():
    db = get_db()
    rst = []
    for post in db.execute(
        "SELECT p.id, title, body, created, author_id, username as author_name"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY p.created DESC, p.id DESC"
    ):
        rst.append(dict(post) | dict(comments=get_all_comments(post["id"])))
    return rst

