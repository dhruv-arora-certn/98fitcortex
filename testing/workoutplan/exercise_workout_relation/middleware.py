import logging

class EDRelationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("django")

    def __call__(self, request):
        print(
            "Calling EDRelationMiddleware"
        )
        print("Authentication ",request.user)
        return self.get_response(request)

