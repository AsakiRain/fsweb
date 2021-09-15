from hashlib import new
from re import A, I
from typing import ItemsView
from sanic import Sanic, app,response
from jinja2 import Environment,FileSystemLoader,select_autoescape
import sys
import json

from sanic.models.handler_types import RequestMiddlewareType
import io_middleware

app = Sanic(__name__)
enable_async = sys.version_info >= (3, 6)
jinja2_env = Environment(
    loader = FileSystemLoader('templates'),
    autoescape=select_autoescape(['html','xml']),
    enable_async=enable_async
)
io_m = None

async def render_template(template_name,**kwargs):
    raw_template = jinja2_env.get_template(template_name)
    print(kwargs)
    rendered_template = await raw_template.render_async(kwargs=kwargs)
    return rendered_template

@app.listener("before_server_start")
async def initialize(app,loop):
    global io_m 
    io_m = io_middleware.IOMiddleware()
    await io_m.init()

@app.route('/')
async def index(request):
    return response.html(await render_template('index.html',notice = 'HelloWorld powered by Sanic'))

@app.route('/signin',methods=['GET','POST'])
async def signin(request):
    if request.method == 'GET':
        return response.html(await render_template('signin.html'))
    elif request.method == 'POST':
        account = request.form.get('account',None)
        password = request.form.get('password',None)
        hidden   = request.form.get('hidden',None)
        if not account or not password:
            return response.text("账号或密码为空")
        else:
            valid,token = await io_m.sign_in(account,password)
            if valid == True:
                return response.html(f"""登录成功！你的token是：{token}""")
            else:
                return response.html(f"""登陆失败！账号或密码错误""")
@app.route('/signup',methods=['GET','POST'])
async def signup(request):
    if request.method == 'GET':
        return response.html(await render_template('signup.html'))
    elif request.method == 'POST':
        account = request.form.get('account',None)
        password = request.form.get('password',None)
        repeat_pass = request.form.get('repeat',None)
        hidden   = request.form.get('hidden',None)
        if not account or not password:
            return response.text("账号或密码为空")
        else:
            if password == repeat_pass:
                valid = await io_m.sign_up(account,password)
                if valid == True:
                    return response.html(f"""注册成功""")
                else:
                    return response.html(f"""注册失败""")
            else:
                return response.text("两次输入密码不一致")
    
@app.route('/api/v0/signin',methods=['POST'])
async def api_signin(request):
    account = request.form.get('account',None)
    password = request.form.get('password',None)
    hidden   = request.form.get('hidden',None)
    if not account or not password:
        return response.json({'result':'fail','detail':'Empty account or password'})
    else:
        valid,token = await io_m.sign_in(account,password)
        if valid == True:
            return response.json({'result':'success','token':token})
        else:
            return response.json({'result':'fail','detail':'Wrong account or passwords'})
@app.route('/api/v0/minecraft/checkbind/<account>',methods=['GET'])
async def api_minecraft_checkbind(request,account):
    result = await io_m.minecraft_checkbind(account)
    if result == 1:
        return response.json({'result':'success','detail':'Verified'})
    elif result == 0:
        return response.json({'result':'success','detail':'Not verified'})
    elif result == 2:
        return response.json({'result':'success','detail':'Not registered'})

@app.route('/api/v0/minecraft/bind/<account>',methods=['GET','POST'])
async def api_minecraft_bind(request,account):
    if request.method == 'GET':
        result,code =  await io_m.minecraft_bind_get(account)
        if result == 0:
            return response.json({'result':'fail','detail':'Already binded'})
        elif result == 1:
            return response.json({'result':'success','detail':'Here is your code.','code':code})


if __name__ == '__main__':
    app.run(host='localhost',port=8090,debug=True)

# @app.route('/testexam')
# async def testexam(request):
#     raw_template = jinja2_env.get_template('testexam.html')
#     a='巴拉巴拉'
#     b='啊吧啊吧'
#     foo='bar'
#     rendered_template = await raw_template.render_async(a=a,b=b,foo=foo)
#     return response.html(rendered_template)

# @app.route('/testtrouble')
# async def testtrouble(request):
#     html =  await render_template('index.html',a='巴拉巴拉',b='啊吧啊吧',foo='bar')
#     return response.html(html)
# async def render_template(template_name,**kwargs):
#     raw_template = jinja2_env.get_template(template_name)
#     rendered_template = await raw_template.render_async(这里不会)
#     return rendered_template
