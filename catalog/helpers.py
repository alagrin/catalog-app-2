from functools import wraps
from flask import session as login_session, request, redirect, url_for
import random

def gen_random_string(valid, length):
        random_string = ''.join(valid)
        return ''.join(random.choice(random_string) for x in range(length))
