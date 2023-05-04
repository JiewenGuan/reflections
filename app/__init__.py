from flask import Flask
from flask_socketio import SocketIO
from secrets import token_hex
from flask_cors import CORS
from .videoManager import VideoManager, Hmd
from flask_bootstrap import Bootstrap5


socketio = SocketIO(cors_allowed_origins='*')

videoManager:VideoManager = VideoManager()
hmds:list[Hmd] = []

def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    # intentionally make old session expire on each rerun
    #app.config['SECRET_KEY'] = token_hex(32)
    app.config['SECRET_KEY'] ="7f7de268f92d245847e5265d5198deabe48f3a97deb26a8527b5c8eff05d51bf"
    CORS(app)
    Bootstrap5(app)

    from .main import main as main_bp
    app.register_blueprint(main_bp)
    from .chat import chat as chat_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')

    socketio.init_app(app)
    return app
