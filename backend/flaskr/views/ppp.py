from flaskr.utils.db import get_db, CTE

posts = [{'author_id': 2, 'author_name': 'aBCs3', 'body': 'abcsfsdfsdfsd', 'comments': [], 'created': 1654483498.0, 'id': 5, 'title': '232'}, {'author_id': 2, 'author_name': 'aBCs3', 'body': 'abcsfsdfsdfsd', 'comments': [], 'created': 1654481475.0, 'id': 4, 'title': '232'}, {'author_id': 1, 'author_name': 'csdfsdfsss', 'body': 'abcsfsdfsdfsd', 'comments': [{'author_id': 2, 'author_name': 'aBCs3', 'body': '000000', 'children': [], 'created': 1654476760.0, 'id': 8, 'parent_id': None, 'post_id': 3, 'tree_path': '8 '}], 'created': 1654474666.0, 'id': 3, 'title': '232'}, {'author_id': 1, 'author_name': 'csdfsdfsss', 'body': 'abcsfsdfsdfsd', 'comments': [], 'created': 1654474655.0, 'id': 2, 'title': '1sdf'}, {'author_id': 1, 'author_name': 'csdfsdfsss', 'body': 'abcsfsdfsdfsd', 'comments': [{'author_id': 1, 'author_name': 'csdfsdfsss', 'body': '000000', 'children': [{'author_id': 1, 'author_name': 'csdfsdfsss', 'body': 'absdsds', 'children': [{'author_id': 1, 'author_name': 'csdfsdfsss', 'body': 'absdsds', 'children': [{'author_id': 1, 'author_name': 'csdfsdfsss', 'body': 'absdsds', 'children': [{'author_id': 1, 'author_name': 'csdfsdfsss', 'body': 'absdsds', 'children': [], 'created': 1654474415.0, 'id': 7, 'parent_id': 4, 'post_id': 1, 'tree_path': '1 2 3 4 7 '}, {'author_id': 2, 'author_name': 'aBCs3', 'body': 'absdsds', 'children': [], 'created': 1654488498.0, 'id': 9, 'parent_id': 4, 'post_id': 1, 'tree_path': '1 2 3 4 9 '}], 'created': 1654472527.0, 'id': 4, 'parent_id': 3, 'post_id': 1, 'tree_path': '1 2 3 4 '}, {'author_id': 1, 'author_name': 'csdfsdfsss', 'body': 'absdsds', 'children': [], 'created': 1654474406.0, 'id': 6, 'parent_id': 3, 'post_id': 1, 'tree_path': '1 2 3 6 '}, {'author_id': 2, 'author_name': 'aBCs3', 'body': 'absdsds', 'children': [], 'created': 1654488545.0, 'id': 10, 'parent_id': 3, 'post_id': 1, 'tree_path': '1 2 3 10 '}], 'created': 1654472526.0, 'id': 3, 'parent_id': 2, 'post_id': 1, 'tree_path': '1 2 3 '}], 'created': 1654472522.0, 'id': 2, 'parent_id': 1, 'post_id': 1, 'tree_path': '1 2 '}], 'created': 1654472510.0, 'id': 1, 'parent_id': None, 'post_id': 1, 'tree_path': '1 '}, {'author_id': 1, 'author_name': 'csdfsdfsss', 'body': '000000', 'children': [], 'created': 1654474321.0, 'id': 5, 'parent_id': None, 'post_id': 1, 'tree_path': '5 '}], 'created': 1654468105.0, 'id': 1, 'title': '1sdf'}]


def rec(_comment: dict, count=1):
    print('<ul>' * count, _comment['id'], _comment['body'])
    for __c_comment in _comment['children']:
        rec(__c_comment, count+1)


for post in posts:
    print(f"{post['id']} {post['title']} {post['body']} {post['created']}")
    for comment in post['comments']:
        rec(comment)
    print('--' * 20)


# CTE_rows = [{'id': 1, 'parent_id': None, 'post_id': 1, 'body': '000000', 'created': 1654472510.0, 'author_id': 1, 'author_name': 'aBCs3', 'tree_path': '1 '}, {'id': 2, 'parent_id': 1, 'post_id': 1, 'body': 'absdsds', 'created': 1654472522.0, 'author_id': 1, 'author_name': 'aBCs3', 'tree_path': '1 2 '}, {'id': 3, 'parent_id': 2, 'post_id': 1, 'body': 'absdsds', 'created': 1654472526.0, 'author_id': 1, 'author_name': 'aBCs3', 'tree_path': '1 2 3 '}, {'id': 4, 'parent_id': 3, 'post_id': 1, 'body': 'absdsds', 'created': 1654472527.0, 'author_id': 1, 'author_name': 'aBCs3', 'tree_path': '1 2 3 4 '}, {'id': 7, 'parent_id': 4, 'post_id': 1, 'body': 'absdsds', 'created': 1654474415.0, 'author_id': 1, 'author_name': 'aBCs3', 'tree_path': '1 2 3 4 7 '}, {'id': 6, 'parent_id': 3, 'post_id': 1, 'body': 'absdsds', 'created': 1654474406.0, 'author_id': 1, 'author_name': 'aBCs3', 'tree_path': '1 2 3 6 '}, {'id': 5, 'parent_id': None, 'post_id': 1, 'body': '000000', 'created': 1654474321.0, 'author_id': 1, 'author_name': 'aBCs3', 'tree_path': '5 '}]
