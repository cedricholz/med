import json

import requests
from decouple import config

from med.settings import ENV


class Api:
    def __init__(self, force_dev=False, force_production=False):
        self.force_dev = force_dev
        self.force_production = force_production

        if force_dev or (not force_production and ENV != 'production'):
            self.sandbox = True
        else:
            self.sandbox = False
        self.timeout = 30
        self.headers = None
        self.proxies = None
        self.access_token = None

    def _get(
            self,
            url: str,
            params: dict = None,
            json_data: dict = None,
            headers: dict = None,
    ) -> dict:
        resp = requests.get(
            url=url,
            params=params,
            json=json_data,
            headers=headers or self.headers,
            timeout=self.timeout,
            proxies=self.proxies,
        )
        resp = self.get_resp_json(resp)
        return resp

    def _post(
            self,
            url: str,
            json_data: dict = None,
            data=None,
            headers: dict = None,
            params: dict = None,
    ) -> dict:
        headers = headers or self.headers
        resp = requests.post(
            url=url,
            json=json_data,
            data=data,
            headers=headers,
            timeout=self.timeout,
            proxies=self.proxies,
            params=params,
        )
        resp = self.get_resp_json(resp)
        return resp

    def _patch(self, url: str, json_data: dict = None, data: dict = None) -> dict:
        resp = requests.patch(
            url=url,
            json=json_data,
            data=data,
            headers=self.headers,
            timeout=self.timeout,
            proxies=self.proxies,
        )
        resp = self.get_resp_json(resp)
        return resp

    def _put(
            self,
            url: str,
            json_data: dict = None,
            data: dict = None,
            params: dict = None,
    ) -> dict:
        resp = requests.put(
            url=url,
            json=json_data,
            data=data,
            params=params,
            headers=self.headers,
            timeout=self.timeout,
            proxies=self.proxies,
        )
        resp = self.get_resp_json(resp)
        return resp

    def _delete(self, url: str, data: dict = None, json_data: dict = None) -> dict:
        resp = requests.delete(
            url=url,
            data=data,
            json=json_data,
            headers=self.headers,
            timeout=self.timeout,
            proxies=self.proxies,
        )
        resp = self.get_resp_json(resp)
        return resp

    def get_resp_json(self, resp):
        try:
            return resp.json()
        except Exception:
            try:
                return json.loads(resp.content)
            except Exception:
                try:
                    return json.loads(resp.text)
                except Exception as exc:
                    return {"reason": resp.reason}
