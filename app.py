# coding: utf-8

import os
import hashlib
import json
import requests
from flask import Flask, request


BOT_URL = os.environ['BOT_URL']
WEBHOOK_SECRET_KEY = os.environ['WEBHOOK_SECRET_KEY']


app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello world'


@app.route('/webhooks/', methods=['POST'])
def webhooks():

    try:

        shop_domain = request.headers.get('X-HeyShop-Shop-Domain', '')
        shop_name = request.headers.get('X-HeyShop-Shop', '')
        event = request.headers.get('X-HeyShop-Event', '')
        hmac_sha256 = request.headers.get('X-HeyShop-Hmac-Sha256', '')

        data = request.data

        show_text = """
        X-HeyShop-Shop-Domain: %s
        X-HeyShop-Shop: %s
        X-HeyShop-Event: %s
        X-HeyShop-Sha256: %s
        data: %s
        """ % (shop_domain, shop_name, event, hmac_sha256, data)

        secret_str = data + WEBHOOK_SECRET_KEY

        if hashlib.sha256(secret_str).hexdigest() == hmac_sha256:

            try:
                data = json.loads(data)
                data = data['data']

                show_text = """
                Paid Success!
                Order Number: %s
                Title: %s
                Customer: %s
                Total Price: %s
                """ % (data['order_number'], data['title'], data['customer']['mobile'], data['total_price'])

                requests.post(url=BOT_URL, json={'text': show_text + 'ok'})

                return 'ok', 200
            except Exception as e:
                requests.post(url=BOT_URL, json={'text': show_text + 'error!\n' + str(e)})
                return 'error', 500

        else:

            requests.post(url=BOT_URL, json={'text': show_text + 'verify failed!'})
            return 'verify failed', 400

    except Exception as e:
        requests.post(url=BOT_URL, json={'text': 'error!!!\n%s' % e})
        raise e


if __name__ == '__main__':
    app.run(debug=True)
