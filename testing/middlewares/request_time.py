import logging
import time

from django.utils.deprecation import MiddlewareMixin

class RequestTimeMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        self.start_time = time.time()

    def process_response(self, request, response):
        logger = logging.getLogger("django.request")
        try:
            req_time = time.time() - self.start_time
            logger.debug("Time to execute request: %f"%req_time, extra = {
                "time" : req_time,
                "path" : request.path,
                "status" : response.status_code
            })
            print("in middleware")
        except Exception as e:
            logging.error("RequestTimeMiddleware Error: %s"%e)
 
        return response

