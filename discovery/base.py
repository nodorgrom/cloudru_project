import requests
import logging
import json
import httpx
import asyncio
from discovery.config import Config

class CloudEvoClient:
    def __init__(self):
        Config.validate()

        self.project_id = Config.PROJECT_ID
        self.api_base = Config.API_BASE_URL

        self._token = self._get_token(Config.CLIENT_ID, Config.CLIENT_SECRET)
        self.headers = {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/json'
        }

    def _get_token(self, key_id, secret):
      try:
        payload = {
          "keyId": key_id,
          "secret": secret
        }

        resp = requests.post(Config.AUTH_URL, json=payload, timeout=Config.GET_TIMEOUT)

        if resp.status_code != 200:
          logging.error(f"Auth failed: {resp.status_code} - {resp.text}")

        token_data = resp.json()
        return token_data.get('access_token')
      except Exception as e:
        logging.error(f"Auth failed {e}")
        raise e


    def perform_request(self, method, api_url, params=None):
        url = api_url

        try:
            resp = requests.request(method, url, headers=self.headers, params=params)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 400:
                logging.warning(f"Wrong request: {url}")
                logging.warning(f"Auth failed: {resp.status_code} - {resp.text}")
                return None
            elif resp.status_code == 404:
                logging.warning(f"Resource not found: {url}")
                return None
            else:
                resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"API Error on {url}: {e}")
            raise


    async def perform_async_request(self, method, url, params=None):
        async with httpx.AsyncClient(headers=self.headers, timeout=Config.GET_TIMEOUT) as client:
            try:
                resp = await client.request(method, url, params=params)
                if resp.status_code == 200:
                    return resp.json()
                return None
            except Exception as e:
                logging.error(f"Async API Error on {url}: {e}")
                return None
