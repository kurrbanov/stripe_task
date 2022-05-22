import logging
import os

from django.http import HttpResponse

error_logger = logging.getLogger('error_logs')
error_handler = logging.FileHandler(
    filename=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs/error.log'))
error_logger.setLevel(logging.ERROR)
error_handler.setFormatter(
    logging.Formatter("%(levelname)s: [%(asctime)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
error_logger.addHandler(error_handler)


class Handle500:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_exception(self, request, exception):
        error_logger.error(exception, exc_info=True)
        return HttpResponse('<h1>500 Internal Server Error</h1>')
