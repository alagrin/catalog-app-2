from flask import Flask, render_template, url_for, request, redirect, flash, \
jsonify, session as login_session, make_response, abort
import random, string, httplib2, json, requests, os
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.client import FlowExchangeError

# CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

app = Flask(__name__)

@app.route('/')
def main():
    pass

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(port=8080, debug=True)
