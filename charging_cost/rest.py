import requests

from charging_cost.settings import DEBUG


class RestUrl:
    SERVER_URL = "http://localhost:8000/rest/" if DEBUG else "https://api.zaptec.com/"
    # Post Request
    # application/x-www-form-urlencoded
    AUTH = "oauth/token/"
    AUTH_URL = SERVER_URL + AUTH
    # Get Request
    # application/json
    CHARGERS = "api/chargers/"
    CHARGERS_URL = SERVER_URL + CHARGERS
    # Post Request
    # application/json
    HISTORY = "api/chargehistory/"
    HISTORY_URL = SERVER_URL + HISTORY

    @staticmethod
    def get_history_url(device_id, start, end):
        return RestUrl.HISTORY_URL + "?ChargerId=" + str(device_id) + "&From=" + str(start) + "&To=" + str(end)


class RestRequest:
    AUTH_GRANT_TYPE = "grant_type"
    AUTH_USERNAME = "username"
    AUTH_PASSWORD = "password"
    AUTH_SCOPE = "scope"
    AUTH_REFRESH_TOKEN = "refresh_token"
    HISTORY_CHARGER_ID = "ChargerId"
    HISTORY_START = "From"
    HISTORY_END = "To"


class RestResponse:
    AUTH_BEARER_TOKEN = "access_token"
    AUTH_REFRESH_TOKEN = "refresh_token"
    DATA = "Data"


class RestError(Exception):
    pass


class RestHeaders:
    AUTH_HEADERS = {'Content-type': 'application/x-www-form-urlencoded'}

    @staticmethod
    def data_headers(bearer):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer
        }


class RestClient:
    @staticmethod
    def auth(username, password):
        params = {
            RestRequest.AUTH_GRANT_TYPE: 'password',
            RestRequest.AUTH_USERNAME: username,
            RestRequest.AUTH_PASSWORD: password,
            RestRequest.AUTH_SCOPE: 'offline_access',
        }
        response = requests.post(RestUrl.AUTH_URL, headers=RestHeaders.AUTH_HEADERS, data=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise RestError()

    @staticmethod
    def refresh(token):
        params = {
            RestRequest.AUTH_GRANT_TYPE: 'refresh_token',
            RestRequest.AUTH_REFRESH_TOKEN: token,
        }
        response = requests.post(RestUrl.AUTH_URL, headers=RestHeaders.AUTH_HEADERS, data=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise RestError()

    @staticmethod
    def chargers(bearer):
        response = requests.get(RestUrl.CHARGERS_URL, headers=RestHeaders.data_headers(bearer))
        if response.status_code == 200:
            return response.json()
        else:
            raise RestError()

    @staticmethod
    def charging_history(bearer, charger_id, start, end):
        response = requests.get(RestUrl.get_history_url(charger_id, start, end),
                                headers=RestHeaders.data_headers(bearer))
        if response.status_code == 200:
            return response.json()
        else:
            raise RestError()
