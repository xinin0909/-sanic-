from sanic import Sanic,blueprints
from sanic.response import text,html,file,json,redirect
from sanic.exceptions import NotFound
from jinja2 import Environment, PackageLoader, select_autoescape
from sanic_auth import Auth, User
from txtindex import Txt2index
from frame_analyze import Application
from showfilepath import showfilepath
import json,os
import logger

env = Environment(loader=PackageLoader('main_blueprint', 'templates'))

simple_value = 0.00
VIRSION = 0.51
session ={}
import asyncio
from sanicdb import SanicDB

env = Environment(
    loader=PackageLoader('main_blueprint', '/templates'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']))

def template(tpl, **kwargs):
    template = env.get_template(tpl)
    return html(template.render(kwargs))

app= Sanic()
app.virsion =VIRSION
app.simple_value = simple_value
app.dong_file_type = ''
app.dong_path = ''
app.dong_yearspath = []
app.static('/static','./static')
auth = Auth(app)
db = SanicDB('localhost', 'chatroom', 'root', "root", sanic=app)


@app.middleware('request')
async def add_session(request):
    request['session'] = session
@app.route('/index')
async def set_index(request):
    return template('index.html')

@app.route('/')
async def index(request):
    # sql = 'select * from user_info where user_id=18'
    # data = await app.db.query(sql)
    # print(data)
    # return json(data)
    logger.logger.info('Here is your log')

    virsion = app.virsion
    print(virsion)
    print(request['session'])
    if '_auth' in request['session']:
          user = request['session']['_auth']
    return template('1.html',title = 'index',cates = locals())

# @app.exception(NotFound)
# def ignore_404_(request):
#     return text('i can not fround ites pages')
@app.route('/login',methods=['POST',"GET"])
async def login(request):
    if request.method=='GET':
        return template('login.html')
    else:
        name = request.form.get('username')
        password = request.form.get('password')
        print(name,password)
        sql = 'select user_id,user_name,user_gender_id from user_info where user_name="%s"'%name
        print(sql)
        data1 = await app.db.query(sql)
        print(data1[0]['user_gender_id'])
        if data1[0]['user_name'] == name and str(data1[0]['user_gender_id']) == password:
            user = User(id=data1[0]['user_id'], name=name)
            auth.login_user(request, user)
            return redirect('/')
        else:
            return text('帐号或密码错误，回去吧！')
        # return redirect('/')
# 调用内置的登出函数，清除session
@app.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return redirect('/')

@app.route('/register',methods=['POST','GET'])
async def user_register(request):
    if request.method =='GET':
        return template('register.html')
    else:
        data = request.json()
        sql = 'insert into %s,%s'%data.args.get('name'),data.args.get('password')
        data = await app.db.query(sql)
        return html("<h1>register success</h1><buttom href ='/mainwindow'>进入</buttom>")

@app.route('/mainwindow')
async def mainwindow_show(request):
    if request.method == 'GET':
        date = request.args.get('cateid')
        simple_value = app.simple_value
        file_type = app.dong_file_type
        print('date',date)
        return template('mainwindow.html',cates = locals())

@app.route('/mainwindow/show')
async def mainwindow(request):
    year_path = app.dong_path
    print(year_path,'sdfsdfsdf')
    dong_yearspath = app.dong_yearspath
    pictype = request.args.get('pictype')
    type1 = request.args.get('type1')
    print(year_path,float(app.simple_value),pictype)
    if app.simple_value == 0.00 or year_path is None:
        return html('')
    else:
        if type1 == '1':
            print('1')
            dong_app = Application(year_path,float(app.simple_value),pictype)
        elif type1 == '2':
            print('2')
            dong_app = Application(dong_yearspath,float(app.simple_value),pictype)
            # print(app.dong_yearspath,app.simple_value,pictype)
    try:
        with open('save.png')as f:
            return await file('save.png')
    except:
        return redirect('/mainwindow')

@app.route('/value',methods=['POST',"GET"])
async def set_value(request):
    if request.method =='GET':
        return template('value.html')
    else:
        simple_value = request.form.get('simple_value')
        logger.logger.info(r"设置地震目录距离:" + str(simple_value))
        app.simple_value = simple_value
        return redirect('/mainwindow')

# 单年文件
@app.route('/year',methods=['GET',"POST"])
async def set_year(request):
    if request.method == 'GET':
        if app.dong_file_type == '':
            return redirect('/mainwindow')
        for asd in app.dong_file_type:
            road = 'data/'+asd
        t1i = Txt2index(datadir=road)
        indexdict = t1i.txt2index()
        year = indexdict['starttime']
        station = indexdict['station']
        dong_datatype = indexdict['type']
        dong_device = indexdict['device']
        file_type = app.dong_file_type
        PATH =showfilepath(file_type).showfile()
        return template('year.html',cates = locals())
    else:
        station = request.form['basestation']
        year = request.form['year']
        dong_datatype = request.form['dong_datatype']
        dong_device = request.form['device']
        if app.dong_file_type ==['dongqi']:
            with open('dataindex.json','r') as f:
                jsons = f.read()
                dong_indexdict = json.loads(jsons)
                print('load '+'dataindex.json')
        elif app.dong_file_type == ['ronjieqidon']:
            with open('ronjiedataindex.json','r') as f:
                jsons = f.read()
                dong_indexdict = json.loads(jsons)
                print('load '+'ronjiedataindex.json')
        dong_name  = 'origin' + '_' + station[0] + '_' + dong_datatype[0] + '_' + dong_device[0] + '_' + year[0]
        print(dong_name)
        app.dong_path = dong_indexdict[dong_name]['filename']
        return redirect('/mainwindow')

# 多年文件
@app.route('/years',methods=['GET',"POST"])
async def set_years(request):
    if request.method == 'GET':
        if app.dong_file_type == '':
            return redirect('/mainwindow')
        for asd in app.dong_file_type:
            road = 'data/' + asd
        t2i = Txt2index(datadir=road)
        indexdict = t2i.txt2index()
        year = indexdict['starttime']
        station = indexdict['station']
        dong_datatype = indexdict['type']
        dong_device = indexdict['device']
        file_type = app.dong_file_type
        PATH = showfilepath(file_type).showfile()
        return template('years.html',cates = locals())
    else:
        #选择一共多少年
        yearsnumber = request.form['yearsnumber']
        print(yearsnumber)
        station = request.form['basestation']
        year = request.form['year'][0].split('-')[0]
        dong_datatype = request.form['dong_datatype']
        dong_device = request.form['device']
        years_filename = []
        # 加载json文件
        with open('dataindex.json','r') as f:
            jsons = f.read()
            dong_indexdict = json.loads(jsons)
            print('load '+'dataindex.json')
        for x in range(0,int(yearsnumber[0])):
            dong_name = 'origin' + '_' + station[0] + '_' + dong_datatype[0] + '_' + dong_device[0] + '_' + str(int(year)+ x)+'-01-01'
            app.dong_yearspath.append(dong_indexdict[dong_name]['filename'])
        print(app.dong_yearspath)
        return redirect('/mainwindow')


@app.route('/dongqi',methods=['GET',"POST"])
async def set_dongqi(request):
    if request.method == 'GET':
        return template('dongqi.html')
    else:
        file_type = request.form['dongqi']
        print(file_type)
        app.dong_file_type = file_type
        logger.logger.info(r"设置数据类型:" + file_type[0])
        return redirect('/mainwindow')

@app.route('/log')
async def set_lig(request):
    with open ('static/log/dongdata.log','r')as p:
        data = p.readlines()
    return text(data)

# # 界面图片路径
# @app.route('/static/images/b.jpg')
# async def picture(request):
#     return await file('static/images/b.jpg')
#
# # 界面css文件路径
# @app.route('/static/css/login_reglogin.css')
# async def login_css(request):
#     return await file('static/css/login_reglogin.css')
#
# @app.route('/static/css/style.css')
# async def login_css(request):
#     return await file('static/css/style.css')



if __name__=='__main__':
    app.run(host="0.0.0.0",port=8000,debug=True)

