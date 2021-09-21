import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)


#############################################################################
############ CONFIGURATIONS (CAN BE SEPARATE CONFIG.PY FILE) ###############
###########################################################################

# Remember you need to set your environment variables at the command line
# when you deploy this to a real website.
# export SECRET_KEY=mysecret
# set SECRET_KEY=mysecret
app.config['SECRET_KEY'] = 'asdflajsdfajkgkagfgfyarylsgdlcfhasvdcyweuhfw834061263472hjklsdfopqwe7'

#################################
### DATABASE SETUPS ############
###############################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app,db)


###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "users.login"

app.jinja_env.filters['zip'] = zip

###########################
#### BLUEPRINT CONFIGS #######
#########################

# Import these at the top if you want
# We've imported them here for easy reference
from myproject.core.views import core
from myproject.users.views import users
from myproject.error_pages.handlers import error_pages
from myproject.beam_posts.views import beam_posts

from myproject.beam_codes.views import beam_codes

from myproject.column_posts.views import column_posts
from myproject.truss_posts.views import truss_posts

# Register the apps
app.register_blueprint(users)
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(beam_posts)
app.register_blueprint(beam_codes)
app.register_blueprint(column_posts)
app.register_blueprint(truss_posts)
