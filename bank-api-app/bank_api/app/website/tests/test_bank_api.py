import os
import sys
import unittest
import requests
from jsonschema import validate
from website.config import Config
from website.unit_api import UnitApi


class TestNewBankApi(unittest.TestCase):
    username = '***'
    password = '***'

    def test_new_user_signup(self):
        user_data = {
            'username': '***',
            'full_name': '***',
            'password': '***',
        }
        contents = requests.post(url=f'http://{Config.NEWBANK_SERVER}:{Config.NEWBANK_API_PORT}/signup',
                                 json=user_data)

        if contents.status_code == 201:
            assert (contents.status_code == 200 or contents.status_code == 201)
        else:
            assert (contents.json()['message'] == 'User already exists. Please Log in.')

    def test_access_token(self):
        contents = requests.post(url=f'http://{Config.NEWBANK_SERVER}:{Config.NEWBANK_API_PORT}/login',
                                 json={'username': TestNewBankApi.username, 'password': TestNewBankApi.password})

        assert 'access_token' in contents.json()
        access_token = contents.json()['access_token']

        contents = requests.get(url=f'http://{Config.NEWBANK_SERVER}:{Config.NEWBANK_API_PORT}/who_am_i',
                                headers={'Authorization': 'Bearer ' + access_token})
        assert (contents.status_code == 200)

    def test_refresh_access_token(self):
        contents = requests.post(url=f'http://{Config.NEWBANK_SERVER}:{Config.NEWBANK_API_PORT}/login',
                                 json={'username': TestNewBankApi.username, 'password': TestNewBankApi.password})

        access_token = contents.json()['access_token']
        refresh_token = contents.json()['refresh_token']

        contents = requests.post(url=f'http://{Config.NEWBANK_SERVER}:{Config.NEWBANK_API_PORT}/refresh',
                                 headers={'Authorization': 'Bearer ' + refresh_token})
        access_token = contents.json()['access_token']
        assert (contents.status_code == 200)

        contents = requests.get(url=f'http://{Config.NEWBANK_SERVER}:{Config.NEWBANK_API_PORT}/protected',
                                headers={'Authorization': 'Bearer ' + access_token}, json={})
        assert (contents.status_code == 200)

    def test_list_unit_transactions(self):
        contents = requests.post(url=f'http://{Config.NEWBANK_SERVER}:{Config.NEWBANK_API_PORT}/login',
                                 json={'username': TestNewBankApi.username, 'password': TestNewBankApi.password})

        access_token = contents.json()['access_token']

        contents = requests.get(url=f'http://{Config.NEWBANK_SERVER}:{Config.NEWBANK_API_PORT}/transactions',
                                headers={'Authorization': 'Bearer ' + access_token})

        assert (contents.status_code == 200)
        data = contents.json()['data']
        schema = UnitApi().transaction_schema()
        for item in data:
            validate(item, schema)
