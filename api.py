import requests

class BlackboardAPI:
    def __init__(self, auth):
        self.auth = auth

    def get(self, endpoint, params=None):
        url = f"{self.auth.base_url}{endpoint}"
        r = requests.get(url, headers=self.auth.headers(), params=params)
        r.raise_for_status()
        return r.json()

    def post(self, endpoint, data):
        url = f"{self.auth.base_url}{endpoint}"
        r = requests.post(url, headers=self.auth.headers(), json=data)
        r.raise_for_status()
        return r.json()

    def put(self, endpoint, data):
        url = f"{self.auth.base_url}{endpoint}"
        r = requests.put(url, headers=self.auth.headers(), json=data)
        r.raise_for_status()
        return r.json()

    def delete(self, endpoint):
        url = f"{self.auth.base_url}{endpoint}"
        r = requests.delete(url, headers=self.auth.headers())
        r.raise_for_status()
        return r.status_code == 204
