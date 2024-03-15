from django.http import HttpRequest

from charging_cost.rest import RestClient


class ZaptecMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)
        return response

    def process_request(self, request: HttpRequest):
        RestClient.refresh(request.user.refresh_token)
        return None
