import time


class RequestTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.monotonic()

        response = self.get_response(request)

        end_time = time.monotonic() - start_time

        response["X-Request-Timing"] = f"{int(end_time * 1000)}ms"
        return response
