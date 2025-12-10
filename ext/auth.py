from flask_login import LoginManager
from ext.models import Usuarios


auth = LoginManager() 
auth.login_view = "auth.login"

auth.user_loader
def load_user(id:int):
    return Usuarios.get_or_none(Usuarios.id == id)

def init_auth(app):

    auth.init_app(app)
    