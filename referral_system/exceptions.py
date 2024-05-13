class AppExceptions(Exception):
    pass


class AppError(AppExceptions):
    pass


class ErrorType:
    TOKEN_ERROR = {
        'status_code': 403,
        'summary': 'Forbidden',
    }

    INVITE_ERROR = {
        'status_code': 404,
        'summary': 'Not Found',
    }