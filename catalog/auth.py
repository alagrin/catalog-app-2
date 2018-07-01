from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import session as login_session
import random, string, 

flow = flow_from_clientsecrets('client_secret.json', '/', '0.0.0.0:8000/oauth')