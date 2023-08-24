import base64
import http.client
import json
import logging
import os
import pathlib
import ssl
from ssl import SSLCertVerificationError

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class STidCore:
    custom_success_codes = (20, 23, 25, 29, 36, 39, 50, 71, 85, 93, 96, 606, 608)

    def __init__(self):
        self.sslContext = self._sslContext()

    @staticmethod
    def _sslContext():
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(cafile=os.path.join(pathlib.Path(__file__).parent.resolve(), "stidmobile-id-com-chain.pem"))
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        return context

    @staticmethod
    def _b64encode(text: str):
        return base64.b64encode(text.encode()).decode()

    @staticmethod
    def _b64decode(text: str):
        return base64.b64decode(text.encode()).decode()

    def _request(self, method: str, url: str, body: str = "", headers: dict = None, token: str = ""):
        log.debug(f"Sending {method} request to /{url}...")
        host_port = 9092
        host_url = "secure.stidmobile-id.com"
        if headers is None:
            headers = {'Content-Type': 'application/json',
                       'Authorization': 'Bearer ' + token}
        conn = http.client.HTTPSConnection(host=host_url, port=host_port, context=self.sslContext)
        try:
            conn.request(method=method, url="/" + url, body=body, headers=headers)
            response = conn.getresponse()
        except http.client.BadStatusLine as e:
            custom_code = int(e.args[0][9:12])
            custom_message = e.args[0][13:-2]
            success = custom_code in STidCore.custom_success_codes
            if success:
                log.debug(f"Response: {custom_code} - {custom_message}")
            else:
                log.warning(f"Response: {custom_code} - {custom_message}")
            return STidCore.STid_response(success=success, status_code=custom_code, content={'Message': custom_message})
        except SSLCertVerificationError as e:
            log.error(f"SSLCertVerificationError: {e.verify_message}")
            return STidCore.STid_response(success=False, status_code=0, content={'error': e.args})
        except Exception as e:
            log.error(f"Response: {e.args}")
            return STidCore.STid_response(success=False, status_code=0, content={'error': e.args})
        code = response.getcode()
        data = response.read().decode()
        try:
            json_data = json.loads(data)
        except json.JSONDecodeError:
            if data[:15] == "<!DOCTYPE html>":
                # data = data.replace("\r\n", "")
                log.error(f"Response: {code} - HTML received")
                return STidCore.STid_response(success=False, status_code=code, content={'error': 'HTML page received'})
            else:
                log.error(f"Response: json decode error - {data}")
                return STidCore.STid_response(success=False, status_code=code, content={'error': 'json decode error'})
        success = 199 < code < 300
        if success:
            log.debug(f"Response: {code} - {data}")
        else:
            log.warning(f"Response: {code} - {data}")
        return STidCore.STid_response(success=success, status_code=code, content=json_data)

    def get_token(self, client_id: str, client_secret: str):
        b46auth = STidCore._b64encode(f"{client_id}:{client_secret}")
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + b46auth
        }
        return self._request(method="POST", url="token", body="grant_type=client_credentials&scope=global", headers=headers)

    def get_sites(self, token: str):
        return self._request(method="GET", url="api/GetSiteListV1/", token=token)

    def get_site_id(self, token: str, site_name: str):
        if not (r := self.get_sites(token=token)):
            return r
        site_id = next((item['SiteId'] for item in r.content if item["SiteName"] == site_name), None)
        if site_id is None:
            r.success = False
            r.content = {'Message': f"Site \"{site_name}\" not found"}
            return r
        r.content = site_id
        return r

    def get_configs(self, token: str, site_id: int):
        return self._request(method="GET", url=f"api/GetReaderConfigurationListV1/?siteId={site_id}", token=token)

    def get_config_id(self, token: str, site_id: int, config_name: str):
        if not (r := self.get_configs(site_id=site_id, token=token)):
            return r
        config_id = next((item['ConfigurationId'] for item in r.content if item["ConfigurationName"] == config_name), None)
        if config_id is None:
            r.success = False
            r.content = {'Message': f"Config \"{config_name}\" not found"}
            return r
        r.content = config_id
        return r

    def get_credits(self, token: str, available: bool = False):
        return self._request(method="GET", url="api/GetAvailableCreditsV1/" if available else "api/GetReservedCreditsV2/", token=token)

    def get_cards(self, token: str, site_id: int):
        return self._request(method="GET", url=f"/api/GetVirtualCardListV2/?siteId={site_id}", token=token)

    def get_card(self, token: str, site_id: int, card_id: int):
        return self._request(method="GET", url=f"api/GetVirtualCardDetailV2/?siteId={site_id}&vcardId={card_id}", token=token)

    def find_card(self, token: str, site_id: int, key: str, value: str, multiple: bool = False, ignore_case: bool = False, partial: bool = False):
        if not (r := self.get_cards(token=token, site_id=site_id)):
            return r
        value = value.lower() if ignore_case else value
        for card in r.content:
            if key in card:
                check_value = str(card[key]).lower() if ignore_case else str(card[key])
                if value == check_value:
                    return STidCore.STid_response(True, 1, card)
        return STidCore.STid_response(False, -1, "No cards found")

    def get_card_by_email(self, email: str, site_id: int, token: str):
        if not (r := self.get_cards(token=token, site_id=site_id)):
            return r
        if isinstance(r.content, list):
            for card in r.content:
                if 'Email' and 'VirtualCardId' in card:
                    if email.lower() == str(card['Email']).lower():
                        return STidCore.STid_response(True, 1, card)

        return STidCore.STid_response(False, -1, "No cards found")

    def add_card(self, token: str, site_id: int, config_id: str, first_name: str, last_name: str, email: str, card_code: str):
        body = json.dumps({
            "siteId": site_id,
            "ConfigurationId": config_id,
            "FirstName": first_name,
            "LastName": last_name,
            "Email": email,
            "PrivateorStidId": card_code
        })
        return self._request(method="POST", url="api/AddVirtualCardV2/", body=body, token=token)

    def _process_cards(self, token: str, site_id: int, card_ids: list | int, url: str, action: str):
        body = json.dumps({
            "siteId": site_id,
            "ids": card_ids if type(card_ids) is list else (card_ids,)
        })
        if r := self._request(method="POST", url=url, body=body, token=token):
            for card in r.content['responseMessage']:
                if card['StatusCode'] in STidCore.custom_success_codes:
                    log.info(f"Card {card['VirtualCardId']} {action} successful: {card['ResponseMessage']}")
                else:
                    log.warning(f"Card {card['VirtualCardId']} {action} failed: {card['ResponseMessage']}")
                    r.success = False
            if type(card_ids) is list:
                r.content = r.content['responseMessage']
            else:
                r.content = r.content['responseMessage'][0]
        return r

    def send_card(self, token: str, site_id: int, card_ids: int | list):
        return self._process_cards(card_ids=card_ids, url="api/SendVirtualCardV1/", action="Send", site_id=site_id, token=token)

    def revoke_card(self, token: str, site_id: int, card_ids: int | list):
        return self._process_cards(card_ids=card_ids, url="api/RevokeVirtualCardV1/", action="Revoke", site_id=site_id, token=token)

    def delete_card(self, token: str, site_id: int, card_ids: int | list):
        return self._process_cards(card_ids=card_ids, url="api/DeleteVirtualCardV1/", action="Delete", site_id=site_id, token=token)

    def remove_card(self, card_id: int | list):
        pass

    class STid_response:
        def __init__(self, success: bool, status_code: int, content):
            self.success = success
            self.status_code = status_code
            self.content = content

        def __bool__(self):
            return self.success

        def __str__(self):
            return str(self.content)

    class STid_exception(Exception):
        pass
