import requests
import time

class BlackboardAuth:
    def __init__(self, key, secret, base_url):
        self.key = key
        self.secret = secret
        self.base_url = base_url.rstrip("/")
        self.token = None
        self.expiry = 0

    def get_token(self):
        """
        Get an OAuth2 token from Blackboard. Returns token or raises exception with full response.
        """
        if not self.token or time.time() >= self.expiry:
            url = f"{self.base_url}/learn/api/public/v1/oauth2/token"
            try:
                resp = requests.post(
                    url,
                    data={"grant_type": "client_credentials"},
                    auth=(self.key, self.secret)
                )
                # Capture 401 or other errors in detail
                if resp.status_code != 200:
                    raise Exception(
                        f"Failed to obtain token: {resp.status_code} - {resp.text}"
                    )
                data = resp.json()
                self.token = data.get("access_token")
                self.expiry = time.time() + int(data.get("expires_in", 0)) - 30
            except requests.RequestException as e:
                raise Exception(f"Network error during token request: {str(e)}")
        return self.token

    def headers(self):
        return {
            "Authorization": f"Bearer {self.get_token()}",
            "Content-Type": "application/json"
        }


class BlackboardAPI:
    def __init__(self, auth: BlackboardAuth):
        self.auth = auth

    def get(self, endpoint, params=None):
        url = f"{self.auth.base_url}{endpoint}"
        try:
            resp = requests.get(url, headers=self.auth.headers(), params=params)
        except requests.RequestException as e:
            # Return mock response with error details
            return type("Resp", (), {
                "status_code": 0,
                "text": f"Network error: {str(e)}",
                "json": lambda: {}
            })()
        return resp

    def post(self, endpoint, json=None):
        url = f"{self.auth.base_url}{endpoint}"
        try:
            resp = requests.post(url, headers=self.auth.headers(), json=json)
        except requests.RequestException as e:
            # Return mock response with error details
            return type("Resp", (), {
                "status_code": 0,
                "text": f"Network error: {str(e)}",
                "json": lambda: {}
            })()
        return resp
