from bottle import app as bottleapp
from bottle import run, route, request, template, static_file, abort
from beaker.middleware import SessionMiddleware
from json import dumps
from random import randint

beaker_opts = {
    'session.type': 'file',
    'session.data_dir': '.',
    'session.auto': True
}

app = SessionMiddleware(bottleapp(), beaker_opts)

@route('/assets/<filename:path>')
def assets(filename):
    return static_file(filename, root='./assets/')

@route('/')
def index():
    s = request.environ['beaker.session']

    s['count'] = 0
    s['num'] = randint(1, 100)
    s['num'] = 87
    s.save()

    return template('index.html', locals())

@route('/get/<num:int>')
def get(num):
    s = request.environ['beaker.session']
    s['count'] += 1
    s.save()
    if s['count'] > 3:
        abort(text='猜太多次囉')
    else:
        if num > s['num']:
            return dumps({"count": s['count'], 'success': False, 'message': "第<strong>{}</strong>次猜測：<strong>{}</strong>，較大！".format(s['count'], num)})
        elif num < s['num']:
            return dumps({"count": s['count'], 'success': False, 'message': "第<strong>{}</strong>次猜測：<strong>{}</strong>，較小！".format(s['count'], num)})
        else: # 三一律！
            return dumps({"count": s['count'], 'success': True, 'message': "第<strong>{}</strong>次猜測：<strong>{}</strong>，較小！".format(s['count'], num)})

run(app=app, port=8787, debug=True, reloader=True, server='meinheld')
