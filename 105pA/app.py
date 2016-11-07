from beaker.middleware import SessionMiddleware
from bottle import app as bottleapp
from bottle import request, route, run, static_file, template, redirect, abort
from pymongo import MongoClient
from utils import pwhash

beaker_opts = {
    'session.type': 'file',
    'session.data_dir': '.',
    'session.auto': True
}

mongo = MongoClient('localhost', 27017)
col = mongo['105pa']['wow']
app = SessionMiddleware(bottleapp(), beaker_opts)

@route('/assets/<filename:path>')
def assets(filename):
    return static_file(filename, root='./assets/')

@route('/')
def index():
    s = request.environ['beaker.session']
    if 'user' in s:
        status = 1 # authenticated
        name = s['user']
    else:
        status = 0 # stranger
        name = ""
    return template('index.html', locals())

@route('/', method='POST')
def login():
    s = request.environ['beaker.session']
    name, passwd = request.POST['name'], request.POST['passwd']
    dbuser = col.find_one({'name': name, 'passwd': pwhash(passwd)})
    if dbuser:
        s['user'] = name
        s.save()
        return 'login success'
    else:
        abort(text='帳號或密碼錯誤！')

@route('/logout')
def logout():
    s = request.environ['beaker.session']
    if 'user' in s:
        del s['user']
        s.save()
        redirect('/')
    else:
        abort(text='您尚未登入！')

@route('/display', method="POST")
def passwd():
    s = request.environ['beaker.session']
    if 'user' in s:
        myinput = request.POST.getunicode('input')
        name = s['user']
        return template("result.html", locals())
    else:
        abort(text='您尚未登入！')

run(app=app, port=8787, debug=True, reloader=True, server='meinheld')
