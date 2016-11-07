from bottle import app as bottleapp, abort, redirect, request, route, run, static_file, template
from pymongo import MongoClient
from datetime import datetime as dt
from re import compile

mongo = MongoClient('localhost', 27017)
col = mongo['105pc']['table']
col2 = mongo['105pc']['data']

@route('/assets/<filename:path>')
def assets(filename):
    return static_file(filename, root='./assets/')

@route('/add')
@route('/add', method="POST")
def add():
    if request.method == "POST":
        name = request.POST.getunicode('name')
        location = request.POST.getunicode('location')
        contact = request.POST.getunicode('contact')

        timestamp = dt.now().timestamp()
        objid = int(col2.find_one()['count'])
        col2.find_one_and_update({}, {'$set': {'count': objid+1}})

        if col.insert_one({'id': objid,
                           'name': name,
                           'location': location,
                           'contact': contact,
                           'timestamp': timestamp}):
            return "success"
    else:
        return template("add.html")

@route('/query')
@route('/query', method="POST")
def query():
    if request.method == "POST":
        name = request.POST.getunicode('name')
        location = request.POST.getunicode('location')
        name, location = compile(r'.*{}.*'.format(name)), compile(r'.*{}.*'.format(location))

        dbobj = list(col.find({'name': name, 'location': location}))
        return template("result.html", locals()) # XHR to div
    else:
        return template("query.html")

@route('/list')
def objlist():
    try:
        dbobj = list(col.find({})) # page separation TBD
    except:
        dbobj = []
    return template("list.html", locals())

@route('/delete')
@route('/delete', method="POST")
def delete():
    if request.method == "POST":
        objid = int(request.POST['id'])

        if col.find_one_and_delete({'id': objid}):
            return "success"
        else:
            abort(text="該遺失物不存在！請重新輸入")
    else:
        return template("delete.html")

@route('/')
def index():
    return template('index.html', locals())

run(app=bottleapp(), port=8787, debug=True, reloader=True, server='meinheld')
