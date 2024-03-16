# coding: utf-8
import time
import hashlib
import hmac
import requests
import json


def gen_sign(method, url, query_string=None, payload_string=None):
    sign_path = "../cred/credentials.json"

    # Read the credentials from the file
    with open(sign_path, 'r') as f:
        data = json.load(f)
        key = data['pub_key']
        secret = data['secret_key']

    t = time.time()
    m = hashlib.sha512()
    m.update((payload_string or "").encode('utf-8'))
    hashed_payload = m.hexdigest()
    s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, t)
    sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
    return {'KEY': key, 'Timestamp': str(t), 'SIGN': sign}

if __name__ == "__main__":
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    # url = '/account/detail'
    url = '/wallet/total_balance'
    query_param = ''
    sign_headers = gen_sign('GET', prefix + url, query_param)
    headers.update(sign_headers)
    r = requests.request('GET', host + prefix + url, headers=headers)
    # print(r.json())
    print(json.dumps(r.json()))