import requests
import json


class WrapperClass:
    def __init__(self):
        self.urls = {
            "STAGE_SANDBOX": "https://api.sb.stag.card91.in",
            "STAGE_LIVE": "https://api.stag.card91.in",
            "PROD_SANDBOX": "https://api-sandbox.card91.io",
            "PROD": "https://api.card91.io",
        }

    def check_payload(self, payload):
        for key, value in payload.items():
            if not value:
                return {
                    "error": f'Key "{key}" is missing or has an empty value',
                    "status": 400,
                }
        return None

    def getCardDetails(self, config=None, payload=None):
        error_response = self.check_payload(payload)

        if error_response:
            return error_response

        card_id = payload["cardId"]
        token = config["token"]
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer{token}",
        }
        requestOptions = {
            "headers": headers,
        }
        env = config["environment"]
        bank_url = self.urls.get(env)

        url = f"{bank_url}/issuance/v1/cards/{card_id}"

        response = requests.get(url, **requestOptions)
        headers_dict = dict(response.headers)
        response_data = {}
        if response.status_code == 200:
            try:
                response_data["Response"] = response.json()
                response_data["Response"]["cardFlags"] = {}
                response_data["Response"]["addresses"] = []
                response_data["Response"]["wallets"] = {}
                response_data["Response"]["createdBy"] = ""
                response_data["Response"]["modifiedBy"] = ""
                response_data["Response"]["expiredBy"] = ""
                response_data["Response"]["modifiedTime"] = ""
                response_data["Response"]["createdTime"] = ""
                print(response_data["Response"])
            except json.JSONDecodeError:
                response_data["Response"] = "Something went wrong"
        else:
            try:
                response_data["Response"] = response.json()
            except json.JSONDecodeError:
                response_data["Response"] = "Something went wrong"

        response_data = {
            "Status": response.status_code,
            "Headers": json.dumps(headers_dict),
            "Response": response_data["Response"],
        }
        return response_data

    def getCardHolderStatus(self, config=None, payload=None):
        error_response = self.check_payload(payload)

        if error_response:
            return error_response

        mobileNo = payload["mobileNo"]
        token = config["token"]
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer{token}",
        }
        requestOptions = {
            "headers": headers,
        }
        env = config["environment"]
        bank_url = self.urls.get(env)
        url = f"{bank_url}/issuance/v1/cardholders/{mobileNo}"

        response = requests.get(url, **requestOptions)
        headers_dict = dict(response.headers)
        response_data = {}
        if response.status_code == 200:
            try:
                response_data["Response"] = response.json()
                response_data["Response"]["createdAt"] = ""
                response_data["Response"]["email"] = ""
                response_data["Response"]["addresses"] = []
                response_data["Response"]["nameOnCard"] = ""
            except json.JSONDecodeError:
                response_data["Response"] = "Something went wrong"
        else:
            try:
                response_data["Response"] = response.json()
            except json.JSONDecodeError:
                response_data["Response"] = "Something went wrong"

        response_data = {
            "Status": response.status_code,
            "Headers": json.dumps(headers_dict),
            "Response": response_data["Response"],
        }
        return response_data

    def loadFundToCard(self, config=None, payload=None):
        error_response = self.check_payload(payload)

        if error_response:
            return error_response

        token = config["token"]
        payload = payload
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer{token}",
        }

        requestOptions = {"headers": headers, "data": json.dumps(payload)}
        env = config["environment"]
        bank_url = self.urls.get(env)

        url = f"{bank_url}/issuance/v1/card/load"

        response = requests.post(url, **requestOptions)
        headers_dict = dict(response.headers)
        response_data = {}
        if response.status_code == 200:
            try:
                response_data["Response"] = response.json()
                response_data["Response"]["wallets"] = [
                    {
                        "amount": wallet["amount"],
                        "balance": "",
                        "walletId": wallet["walletId"],
                    }
                    for wallet in response_data["Response"]["wallets"]
                ]
            except json.JSONDecodeError:
                response_data["Response"] = "Something went wrong"
        else:
            try:
                response_data["Response"] = response.json()
            except json.JSONDecodeError:
                response_data["Response"] = "Something went wrong"

        response_data = {
            "Status": response.status_code,
            "Headers": json.dumps(headers_dict),
            "Response": response_data["Response"],
        }
        return response_data

    def cardLockOrUnlock(self, config=None, payload=None):
        error_response = self.check_payload(payload)

        if error_response:
            return error_response
        error_response = self.check_payload(payload)

        if error_response:
            return error_response
        token = config["token"]

        payload = payload

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer{token}",
        }

        requestOptions = {"headers": headers, "data": json.dumps(payload)}
        env = config["environment"]
        bank_url = self.urls.get(env)

        url = f"{bank_url}/issuance/v1/card/lock"

        response = requests.put(url, **requestOptions)
        headers_dict = dict(response.headers)
        response_data = {}
        try:
            response_data["Response"] = response.json()
        except json.JSONDecodeError:
            response_data["Response"] = "Something went wrong"
        response_data = {
            "Status": response.status_code,
            "Headers": json.dumps(headers_dict),
            "Response": response_data["Response"],
        }
        return response_data

    def getAddress(self, config=None, payload=None):
        error_response = self.check_payload(payload)

        if error_response:
            return error_response
        customerId = payload["customerId"]
        token = config["token"]

        payload = payload

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer{token}",
        }

        requestOptions = {
            "headers": headers,
        }
        env = config["environment"]
        bank_url = self.urls.get(env)

        url = f"{bank_url}/issuance/v1/addresses/{customerId}/CUST"

        response = requests.get(url, **requestOptions)
        headers_dict = dict(response.headers)
        response_data = {}
        try:
            response_data["Response"] = response.json()
        except json.JSONDecodeError:
            response_data["Response"] = "Something went wrong"
        response_data = {
            "Status": response.status_code,
            "Headers": json.dumps(headers_dict),
            "Response": response_data["Response"],
        }
        return response_data

    def printCard(self, config=None, payload=None):
        error_response = self.check_payload(payload)

        if error_response:
            return error_response
        token = config["token"]

        payload = payload

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer{token}",
        }

        requestOptions = {"headers": headers, "data": json.dumps(payload)}
        env = config["environment"]
        bank_url = self.urls.get(env)

        url = f"{bank_url}/issuance/v1/card/print"

        response = requests.put(url, **requestOptions)
        headers_dict = dict(response.headers)
        response_data = {}
        try:
            response_data["Response"] = response.json()
        except json.JSONDecodeError:
            response_data["Response"] = "Something went wrong"
        response_data = {
            "Status": response.status_code,
            "Headers": json.dumps(headers_dict),
            "Response": response_data["Response"],
        }
        return response_data

    def mapCustomersToInstaKit(self, config=None, payload=None):
        error_response = self.check_payload(payload)

        if error_response:
            return error_response
        token = config["token"]

        payload = payload

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer{token}",
        }

        requestOptions = {"headers": headers, "data": json.dumps(payload)}
        env = config["environment"]
        bank_url = self.urls.get(env)

        url = f"{bank_url}/issuance/v1/cardholders/map"

        response = requests.post(url, **requestOptions)
        headers_dict = dict(response.headers)
        response_data = {}
        try:
            response_data["Response"] = response.json()
        except json.JSONDecodeError:
            response_data["Response"] = "Something went wrong"
        response_data = {
            "Status": response.status_code,
            "Headers": json.dumps(headers_dict),
            "Response": response_data["Response"],
        }
        return response_data


Card91BusinessSDK = WrapperClass()
