from flask import Flask
from src.my_package.models.models import db
from src.my_package.views.folder_validation import validation_views
from src.my_package.views.selection import selection_views
from src.my_package.views.model_interaction import model_interaction_views

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ML_Models.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = '&^\xc9\xc5\x93\x8f+Ll\r\xaa\xc2BFD\x05'
db.init_app(app)

app.register_blueprint(validation_views)
app.register_blueprint(selection_views)
app.register_blueprint(model_interaction_views)
app.template_folder = 'F:\\FULL PROJECT\\src\\my_package\\templates'
app.static_folder = 'F:\\FULL PROJECT\\src\\my_package\\static'