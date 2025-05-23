from django.http import JsonResponse

from exceptions import AppError


class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    def process_exception(request, exception):
        error_data = exception.args[0]
        if isinstance(exception, AppError):
            return JsonResponse(
                data={
                    'description': exception.args[0]['description'],
                    'summary': error_data['error_type']['summary'],
                    'status_code': error_data['error_type']['status_code']
                },
                status=error_data['error_type']['status_code']
            )