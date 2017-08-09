# coding: utf-8

import hashlib
import json
import requests
from flask import Flask, request


webhook_secret_key = '6d913186b7de89e12eeb'
bot_url = 'https://hook.bearychat.com/=bw90f/incoming/3eb2aa1de9e5e6f2d57260e258e92ec6'

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello world'


@app.route('/webooks/', methods=['POST'])
def wehbooks():

    shop_domain = request.headers.get('X-HeyShop-Shop-Domain', '')
    shop_name = request.headers.get('X-HeyShop-Shop', '')
    event = request.headers.get('X-HeyShop-Event', '')
    hmac_sha256 = request.headers.get('X-HeyShop-Hmac-Sha256', '')

    data = request.data

    show_text = """
    X-HeyShop-Shop-Domain: %s,
    X-HeyShop-Shop: %s,
    X-HeyShop-Event: %s,
    X-HeyShop-Hmac-Sha256: %s,
    data: %s,
    """ % (shop_domain, shop_name, event, hmac_sha256, data)

    secret_str = data + webhook_secret_key

    if hashlib.sha256(secret_str).hexdigest() == hmac_sha256:

        requests.post(url=bot_url, json={'text': show_text + 'ok'})

        data = json.loads(data)
        print data

        return 'ok', 200

    else:

        requests.post(url=bot_url, json={'text': show_text + 'verify failed!'})
        return 'verify failed', 400


if __name__ == '__main__':
    app.run(debug=True)
