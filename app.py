from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from whooshalchemy import IndexService

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
#app.config["WHOOSH_BASE"] = "/tmp/whoosh"

db = SQLAlchemy(app)

import routes

#from admin.admin import admin
#app.register_blueprint(admin, url_prefix='/admin')

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Flask and Flask-SQLAlchemy initialization here

from models import Theatres

#admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin = Admin(app, name='', base_template='admin/base_admin_flask.html')

class MyModelView(ModelView):
    edit_template = 'admin.model.list.html'

class TheatreView(MyModelView):
    print('here')
    column_searchable_list = ['name', 'address', 'description']
    column_filters = ['name', 'address', 'description']
    #column_editable_list = ['name', 'address', 'description']
    #column_default_sort = ['name']




admin.add_view(TheatreView(Theatres, db.session, name='Театры', menu_icon_type='image', menu_icon_value='admin/sitepics/building.svg'))



