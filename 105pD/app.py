from bottle import app as bottleapp, abort, redirect, request, route, run, static_file, template
import os
import csv

@route('/assets/<filename:path>')
def assets(filename):
    return static_file(filename, root='./assets/')

@route('/fintech/<filename:path>')
def fintech(filename):
    return static_file(filename, root='./fintech/')

@route('/generator')
@route('/generator', method="POST")
def generator():
    if request.method == "POST":
        number = int(request.POST['number'])
        filename = request.POST.getunicode('filename')
        count = int(request.POST['count'])

        table = [(i, 25+((i+47*i)%45), 15000+((9797*i)%65000), 500+((797*i*i)%950000), 2000+((97*i*i*i+97*i*i)%950000), 4500+((20000+97*i*i)%35000)) for i in range(1,number+1)]

        with open(os.path.join(os.path.curdir, 'fintech', filename), 'w') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
            for x in table:
                writer.writerow(x)
            f.close()

        with open(os.path.join(os.path.curdir, 'fintech', filename), 'r') as f:
            data = '\n'.join(f.readlines()[:count])
        url = request.url.split('generator')[0] + 'fintech/{}'.format(filename)
        return template('gen_result.html', locals())
    else:
        return template('generator.html', locals())

@route('/analytics')
@route('/analytics', method="POST")
def analytics():
    if request.method == "POST":
        url = request.POST.getunicode('url')
        threshold = int(request.POST['threshold'])
        count = int(request.POST['count'])

        with open(url.replace('http://localhost:8787/', './'), 'r') as f:
            res = f.read()
        table = [[int(y) for y in x.replace('\r','').split(',')] for x in res.split('\n')[:-1]]
        newtable = [x + [round((50*x[1])/75-(50*x[2])/80000-(60*(x[3]-x[4]))/60000+(40*x[5])/50000)] for x in table]
        newtable = [x for x in newtable if x[6] >= threshold]

        newtable = newtable[:count+1]
        return template('ana_result.html', locals())
    else:
        return template('analytics.html', locals())

@route('/')
def index():
    return template('index.html', locals())

run(app=bottleapp(), port=8787, debug=True, reloader=True, server='meinheld')
