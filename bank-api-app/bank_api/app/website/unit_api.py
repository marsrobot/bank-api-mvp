import os
import requests
import pprint
from website.config import Config

os.environ['READ_TOKEN'] = Config.UNIT_READ_TOKEN
os.environ['WRITE_TOKEN'] = Config.UNIT_WRITE_TOKEN
os.environ['api_url'] = f'{Config.UNIT_SERVER}/transactions?filter[type][0]=CardTransaction'


class UnitApi:
    def __init__(self):
        pass

    def list_transactions(self):
        url = os.environ['api_url']
        unit_read_token = os.environ['READ_TOKEN']
        contents = requests.get(url=url, headers={'Authorization': 'Bearer ' + unit_read_token})
        # access_token = contents.json()

        print(contents.status_code)
        js = contents.json()
        data = js['data']
        pprint.pprint(data)

        return data

    def transaction_schema(self):
        """
            1. Removed Reference "$ref" to simplify the validation
            2. Changed "additionalProperties" from False to True
            3. Changed
                "internationalServiceFee": {
                    "type": "integer"
                },
            to
                "internationalServiceFee": {
                    "type": ["integer", "null"]
                },
        """
        schema = {
            "title": "Sandbox Card Transaction",
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "const": "cardTransaction"
                },
                "attributes": {
                    "type": "object",
                    "properties": {
                        "createdAt": {
                            "type": "string",
                            "format": "date-time"
                        },
                        "amount": {
                            "type": "integer"
                        },
                        "direction": {
                            "type": "string",
                            "enum": [
                                "Credit",
                                "Debit"
                            ]
                        },
                        "balance": {
                            "type": "integer"
                        },
                        "summary": {
                            "type": "string"
                        },
                        "cardLast4Digits": {
                            "type": "string",
                            "pattern": "^\\d{4}$"
                        },
                        "internationalServiceFee": {
                            "type": ["integer", "null"]
                        },
                        "recurring": {
                            "type": "boolean"
                        },
                    },
                    "required": [
                        "createdAt",
                        "amount",
                        "direction",
                        "balance",
                        "cardLast4Digits",
                        "merchant",
                        "recurring"
                    ],
                    "additionalProperties": True
                },
            },
            "additionalProperties": True,
            "required": [
                "type",
                "id",
                "attributes",
                "relationships"
            ]
        }
        return schema
