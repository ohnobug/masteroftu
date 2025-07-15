import copy
import json
import random
from baidubce.auth import bce_credentials
from baidubce import bce_base_client, bce_client_configuration
from baidubce.http import bce_http_client, handler
from baidubce.services.sms.sms_client import SmsClient
import os

AK = os.getenv("BAIDU_SMS_AK")
SK = os.getenv("BAIDU_SMS_SK")
ENDPOINT = os.getenv("BAIDU_SMS_ENDPOINT")

# 生成一个介于 100000 和 999999 之间的随机整数
def generate_numeric_code_randint():
    code = random.randint(100000, 999999)
    return code

class Sample(bce_base_client.BceBaseClient):
    def __init__(self, config):
        self.config = copy.deepcopy(bce_client_configuration.DEFAULT_CONFIG)
        self.config.merge_non_none_values(config)

    def _send_request(self, http_method, path, headers=None, params=None, body=None):
        return bce_http_client.send_request(
            self.config,
            SmsClient._bce_sms_sign,
            [handler.parse_error, handler.parse_json],
            http_method,
            path,
            body,
            headers,
            params
        )

    def send_register_verify_code(self, phone_number: str, code: str):
        path = b'/api/v3/sendSms'
        headers = {
            b'Content-Type': 'application/json',
            b'Accept': 'application/json'
        }

        params = {"clientToken": str(generate_numeric_code_randint())}
        payload = json.dumps({
            "mobile": phone_number,
            "signatureId": "sms-sign-fUbUik38720",
            "template": "sms-tmpl-nPGFCf77936",
            "contentVar": {
                "SMSvCode": str(code)
            }
        }, ensure_ascii=False)
        return self._send_request(b'POST', path, headers, params, payload.encode('utf-8'))


    def send_reset_password_verify_code(self, phone_number: str, code: str):        
        path = b'/api/v3/sendSms'
        headers = {
            b'Content-Type': 'application/json',
            b'Accept': 'application/json'
        }

        params = {"clientToken": str(generate_numeric_code_randint())}
        payload = json.dumps({
            "mobile": phone_number,
            "signatureId": "sms-sign-fUbUik38720",
            "template": "sms-tmpl-BhwwSS61703",
            "contentVar": {
                "SMSvCode": str(code)
            }
        }, ensure_ascii=False)
        return self._send_request(b'POST', path, headers, params, payload.encode('utf-8'))


config = bce_client_configuration.BceClientConfiguration(
    credentials=bce_credentials.BceCredentials(AK, SK),
    endpoint=ENDPOINT
)

BAIDUSMS = Sample(config)

if __name__ == '__main__':
    config = bce_client_configuration.BceClientConfiguration(
        credentials=bce_credentials.BceCredentials(AK, SK),
        endpoint=ENDPOINT
    )
    client = Sample(config)
    res = client.send_register_verify_code("18825130917", "654321")
    print(res.__dict__)

    res = client.send_reset_password_verify_code("18825130917", "123456")
    print(res.__dict__)
