class PrintMessageException(Exception):
    message = "error message"


class ClassStudentException(PrintMessageException):
    message = "Something went wrong it is likely that this error was caused because you are a student and not a teacher in this classroom."


class WrongUrlEnteredException(PrintMessageException):
    message = "Invalid URL entered for the Discord URL"


class LoginScopeError(PrintMessageException):
    message = "Please give all permissions when logging in and try logging in again"

class LoginError(Exception):
    pass