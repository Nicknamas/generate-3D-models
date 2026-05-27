from werkzeug.exceptions import HTTPException


class UserNotFound(HTTPException):
    code = 404
    description = "User not found"

class UserSessionNotFound(HTTPException):
    code = 404
    description = "User session not found"


class IncorrectEmailOrUsernameException(HTTPException):
    code = 400
    description = "Wrong username or password"


class EmptyEmailException(HTTPException):
    code = 400
    description = "Empty email"


class EmptyPasswordException(HTTPException):
    code = 400
    description = "Empty password"
