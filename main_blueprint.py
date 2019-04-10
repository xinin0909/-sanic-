# from sanic import Blueprint
#
# from sanic.response import json, text, html
#
#
#
# ## Jinja2 template ####
#
# from jinja2 import Environment, PackageLoader
#
# env = Environment(loader=PackageLoader('main_blueprint', 'templates'))
#
#
#
# ## database ####
#
# import uvloop, peewee
#
# from peewee_async import PostgresqlDatabase
#
#
#
# bp = Blueprint('main_blueprint')
#
#
#
# # init db connection
#
# global database
# database = PostgresqlDatabase(database='webdb',
#                               host='127.0.0.1',
#                               user='postgres',
#                               password='111111')
#
#
# # router define
# @bp.route('/')
# async def bp_root(request):
#     serialized_obj = []
#     cursor = database.execute_sql('select * from t1;')
#     for row in cursor.fetchall():
#          serialized_obj.append({
#             'id': row[0],
#             'name': row[1]}
#         )
#     template = env.get_template('index.html')
#     content=template.render(items=serialized_obj)
#     return html(content)