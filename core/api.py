import requests
from datetime import datetime
from django.utils.timezone import make_aware, utc


class FT_API():
    def __init__(self, api_uid, api_secret, **kwargs):
        self.api_uid = api_uid
        self.api_secret = api_secret
        self.base_url = "https://api.intra.42.fr/v2"
        self.token = self.get_oauth_token(**kwargs)
        self.headers = {'Authorization': 'Bearer ' + self.token}

    def get_oauth_token(self, **kwargs):
        url = self.base_url + '/oauth/token'
        post_data = {
            'grant_type': 'client_credentials',
            'client_id': self.api_uid,
            'client_secret': self.api_secret
        }
        post_data.update(kwargs)
        resp = requests.post(url, data=post_data)
        print(resp.text)
        print(resp.request.body)
        return resp.json()['access_token']

    def get_events(self, campus_id=None, cursus_id=None, page=1, page_size=100):
        url = self.base_url
        if campus_id is not None:
            url += '/campus/' + str(campus_id)
        if cursus_id is not None:
            url += '/cursus/' + str(cursus_id)
        url += f'/events?page={page}&per_page={page_size}'
        resp = requests.get(url, headers=self.headers)
        return resp.json()

    def get_campus(self, campus_id):
        url = self.base_url + f'/campus/{campus_id}'
        resp = requests.get(url, headers=self.headers)
        return resp.json()

    def get_cursus(self, cursus_id):
        url = self.base_url + f'/cursus/{cursus_id}'
        resp = requests.get(url, headers=self.headers)
        return resp.json()

    def get_user(self, user_id):
        url = self.base_url + f'/users/{user_id}'
        resp = requests.get(url, headers=self.headers)
        return resp.json()

    def get_me(self):
        url = self.base_url + '/me'
        resp = requests.get(url, headers=self.headers)
        return resp.json()

    def parse_date(self, date):
        return make_aware(datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ'), utc) if date is not None else None
