from tree_ai.core.db.session import engine
from tree_ai.core.db.base_models import Base
from tree_ai.domains.users.api import router as user_router
from flask import Flask

app = Flask(__name__)

app.register_blueprint(user_router)


with app.app_context():
    Base.metadata.create_all(engine)
