from flask import request

def filterByCategory():
    ''' will be using all items'''
    select = request.form.get('categories')
    return select
