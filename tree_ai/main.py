from tree_ai.core.db.session import engine
from tree_ai.core.db.base_models import Base
from tree_ai.core.exceptions import EmptyEmailException
from tree_ai.domains.users.api import router as user_router
from tree_ai.domains.sessions.api import router as session_router
from tree_ai.domains.security.api import router as security_router

from flask import Flask
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

app.register_blueprint(user_router)
app.register_blueprint(session_router)
app.register_blueprint(security_router)


with app.app_context():
    Base.metadata.create_all(engine)


@app.errorhandler(404)
def handle_not_found_error(error):
    return {
        "success": False,
        "error": {
            "code": "NOT_FOUND",
            "message": "The requested URL or resource was not found."
        }
    }, 404


@app.errorhandler(HTTPException)
def handle_unexpected_error(error):
    if isinstance(error, HTTPException):
        return {
            "success": False,
            "error": {
                "code": error.name.upper().replace(" ", "_"), 
                "message": error.description
            }
        }, error.code or 500
        
    return {
        "success": False,
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred on the server."
        }
    }, 500
