import logging
import requests
from requests.adapters import HTTPAdapter, Retry
from .exceptions import BadAuthRequest, KeyNotFound


class AbstractClient:
    def __init__(self, key: str = None, token: str = None, log_level=logging.WARNING):

        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)
        self.logger.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(name)-12s %(funcName)-20s %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self._session = requests.session()
        basic_retries = Retry(total=3,
                              backoff_factor=0.3,
                              status_forcelist=[500, 502, 503, 504])
        auth_retries = Retry(total=3,
                             backoff_factor=0.3,
                             status_forcelist=[500, 502, 503, 504],
                             allowed_methods=["GET", "POST"])
        self._base = f"https://api.dependency.health/v1"
        self._session.mount(self._base, HTTPAdapter(max_retries=basic_retries))
        self._session.mount(self._base + "/auth", HTTPAdapter(max_retries=auth_retries))

        self._key = key
        if token is not None:
            self._token = token
            self._session.headers["Authorization"] = f"Bearer {self._token}"
        else:
            self._login()

        self._system = None  # Should be defined on a subclass level

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._session.close()

    def __del__(self):
        self._session.close()

    # noinspection PyMethodParameters
    def _auth(func):
        def wrapper(self, *args, **kwargs):
            # noinspection PyCallingNonCallable
            response = func(self, *args, **kwargs)
            if response.status_code == 403:
                self._login()
                # noinspection PyCallingNonCallable
                response = func(self, *args, **kwargs)

            return response

        return wrapper

    def _login(self):
        self.logger.debug(f"Logging in ...")
        path = "/auth/login"
        r = self._session.post(self._base + path, json={"key": self._key})

        if r.status_code == 400:
            raise BadAuthRequest
        elif r.status_code == 404:
            raise KeyNotFound
        elif r.status_code == 200:
            r_json = r.json()
            if "token" in r_json.keys() and r_json["token"]:
                self._token = r_json["token"]
                self._session.headers["Authorization"] = f"Bearer {self._token}"
                self.logger.debug(f"Logged in successfully")
            else:
                self.logger.debug(f"Got auth response with no token. \nResponse: {r}")
        else:
            self.logger.debug(f"Got unexpected response code {r.status_code}. \nResponse:{r}")

    @_auth
    def _request(self, *args, **kwargs):
        method = args[0]
        path = args[1]
        params = kwargs.pop("params", None)
        self.logger.debug(f"{method} request {self._base + path}")

        if params is None:
            params = dict()

        if method == "GET":
            return self._session.get(self._base + path, params=params)
        elif method == "POST":
            return self._session.post(self._base + path, json=params)
        else:
            raise NotImplementedError

    def check_package(self, package: str):
        self.logger.debug(f"Getting info for package {package}")

        path = f"/systems/{self._system}/packages/{package}"
        r = self._request("GET", path)

        self.logger.debug(f"Got code {r.status_code}")
        if r.status_code == 200:
            return r.json()
