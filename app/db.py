import sqlite3
import os
# import click
# from flask import current_app, g
# from flask.cli import with_appcontext

DATABASE = "{}/{}".format(os.path.normpath(os.getcwd() + os.sep + os.pardir),'esystem.db')
# print(DATABASE)
# DATABASE = "esystem.db"
def get_db_connection():
    conn = sqlite3.connect("../esystem.db")
    conn.row_factory = sqlite3.Row
    return conn

# def get_db():
#     if 'db' not in g:
#         g.db = sqlite3.connect(
#             DATABASE,
#             detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite3.Row
#
#     return g.db
#
# def query_db(query, args=(), one=False):
#     cur = get_db().execute(query, args)
#     rv = cur.fetchall()
#     cur.close()
#     return (rv[0] if rv else None) if one else rv
#
# def close_db(e=None):
#     db = g.pop('db', None)
#
#     if db is not None:
#         db.close()
#
#
# def init_app(app):
#     app.teardown_appcontext(close_db)