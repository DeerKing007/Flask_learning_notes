# Flask

## 状态保持

> http请求是无状态，当需要在多个请求之间共享数据时，需要引入 cookie  session

### cookie

> 1. 生成在服务器，随着响应到达浏览器随之存储在浏览器的小段数据
>
> 2. 保持数据，使得数据在一段时间之内，可以反复使用**(记住我)**
>
> 3. cookie会随着后续的每一个请求，再次回到服务器
>
>    向服务器发送请求时，会自动携带来自该服务器的所有cookie

```python
@app.route("/cook/")
def testcookie():#写
    response = make_response(render_template("xxx.html")) #获得response
    #response = make_response("Hello World~~") #获得response
    #设置cookie,如果不设置max_age,则为会话cookie
    response.set_cookie("name2","臧红久",max_age=60*10) #设置一个10min的cookie
    return response
@app.route("/cook2/")
def testcookie2():#读
    print(request.cookies.get("name2")) #获取cookie
    return "aaa"

@app.route("/cook3/")
def testcookie3():#删
    response = make_response("hello") #获得response
    #response.delete_cookie('name') #删除cookie
    response.set_cookie("name2",max_age=0) #删除cookie
    return response
```

###session

> 数据保持：同一个会话中多个请求间的数据共享

####client-session(了解)

> flask默认的session处理是将session存在cookie中：“客户端session”
>
> 将session加密后，存于浏览器的cookie中

```python
import os
os.urandom(20) #获得一个随机的key
```

```python
from flask import session
app.secret_key=b'\x19M\xf1\xb2<&\xe2\x16l\x81\xa7G\xe2\xf2"\x82\xe2 d,' #设置加密cookie的密钥
...

@app.route('/z/<reg9("\d+[c-z]+"):name>')
def hello_world(name):
    session['name']="zhj" #数据会加密后存在客户端的cookie中
    return 'Hello World!'
```

####server-session(主流)

> 安装Flask扩展  `pip install flask-session`
>
> 帮助实现sever-session(mysql,redis)

#####session-mysql

```python
from flask_session import Session

#mysql配置
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:222222@localhost/test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True #避免警告信息
db = SQLAlchemy(app) #构建SQLAlchemy对象

#session配置
app.config["SESSION_TYPE"]="sqlalchemy" #session存储类型
app.config["SESSION_SQLALCHEMY"]=db #session存储时，可以使用的SQLAlchemy对象
app.config["SESSION_SQLALCHEMY_TABLE"]='sessions125' #存储session数据的数据表
app.config["SESSION_PERMANENT"]=False #False = 浏览器关闭session失效
#如果会话一直没有活动，30分钟sesison失效，仅适用于SESSION_PERMANENT=True时
#app.config["PERMANENT_SESSION_LIFETIME"]=60*30
app.config["SESSION_USE_SIGNER"]=False #是否需要加密cookie
app.config["SESSION_KEY_PREFIX"]="zhj:" #sessionID的前缀（sessionid会存入数据库中会追加一个prefix）

Session(app) #构建Session，则之后，在项目中可以使用session了

def hello_world(name):
    session['name']="zhj" #数据存入数据库
    return 'Hello World!'

def hello_world2(name):
    session['name'] #从session取数据
    return 'Hello World!'
```

> 注意，在使用session前，需要做一次 `db.create_all()` 保证sessions表被创建(ops:也可以自己手动建表)
>
> ```python
> >>> from app import db
> >>> db.create_all()
> ```

> 补充 : 在session存入mysql的解决方案中，如果是浏览器关闭session失效的情况，需要如下定制
>
> ```python
> #自定义SqlAlchemySessionInterface的open_session逻辑(去掉其中比对是否时间过期逻辑)
> class MySessionInterface(SqlAlchemySessionInterface):
>     def open_session(self, app, request):
>         sid = request.cookies.get(app.session_cookie_name)
>         if not sid:
>             sid = self._generate_sid()
>             return self.session_class(sid=sid, permanent=self.permanent)
>         if self.use_signer:
>             signer = self._get_signer(app)
>             if signer is None:
>                 return None
>             try:
>                 sid_as_bytes = signer.unsign(sid)
>                 sid = sid_as_bytes.decode()
>             except BadSignature:
>                 sid = self._generate_sid()
>                 return self.session_class(sid=sid, permanent=self.permanent)
>
>         store_id = self.key_prefix + sid
>         saved_session = self.sql_session_model.query.filter_by(
>             session_id=store_id).first()
>         #注释掉此 if代码块，其他代码不变 
>         #if saved_session and saved_session.expiry <= datetime.utcnow():
>         #     # Delete expired session
>         #     self.db.session.delete(saved_session)
>         #     self.db.session.commit()
>         #     saved_session = None
>         if saved_session:
>             try:
>                 val = saved_session.data
>                 data = self.serializer.loads(want_bytes(val))
>                 return self.session_class(data, sid=sid)
>             except:
>                 return self.session_class(sid=sid, permanent=self.permanent)
>         return self.session_class(sid=sid, permanent=self.permanent)
>
> #为了让自己的sessioninterface生效，需要：
> #1. Session(app)#为app指定一个server-session的解决方案  必须去掉此句
> #2. 手动指定，Flask实例的session解决方案
> app.session_interface=MySessionInterface(
>                 app, db,
>                 app.config['SESSION_SQLALCHEMY_TABLE'],
>                 app.config['SESSION_KEY_PREFIX'], app.config['SESSION_USE_SIGNER'],
>                 app.config['SESSION_PERMANENT'])
> ```
>

##### session-redis （大型项目，建议使用）

```python
app.config['SESSION_TYPE'] = 'redis'  # session类型为redis
app.config['SESSION_PERMANENT'] = False  # 关闭浏览器session就失效。
#如果会话一直没有活动，30分钟sesison失效
#在redis的解决方案中SESSION_PERMANENT=False和PERMANENT_SESSION_LIFETIME可以共存
app.config["PERMANENT_SESSION_LIFETIME"]=60*30
app.config['SESSION_USE_SIGNER'] = False  # 是否对发送到浏览器上session的cookie值进行加密
app.config['SESSION_KEY_PREFIX'] = 'zhj:'  # 保存到session中的值的前缀
# 用于连接redis的配置  （ops: pip install redis）
app.config['SESSION_REDIS'] = redis.Redis(host='192.168.180.131', port='7000',db=1)  

Session(app) #构建Session

def hello_world(name):
    session['name']="zhj" #数据存入redis
    return 'Hello World!'
```

##静态资源

> flask静态资源根目录是 Flask初始化的目录下的static目录
>
> flask_hello
> ​         ...
> ​         --static
> ​            --hello
> 	       --app.png 

```python
<img src="/static/hello/app.png"/>

#                    /static/hello/app.png
<img src="{{ url_for('static',filename='hello/app.png')}}"/>

#如下view时flask内置的veiw：用于反向解析到静态资源的路径
@app.route("/static/<filename>/")
def static(filename):
    ....

```

##响应json -Json.dumps()

```python
json.dumps()可识别的数据类型：
    +-------------------+---------------+
    | Python            | JSON          |
    +===================+===============+
    | dict              | object        |
    +-------------------+---------------+
    | list, tuple       | array         |
    +-------------------+---------------+
    | str               | string        |
    +-------------------+---------------+
    | int, float        | number        |
    +-------------------+---------------+
    | True              | true          |
    +-------------------+---------------+
    | False             | false         |
    +-------------------+---------------+
    | None              | null          |
与django中，使用JsonResponse不同的是：
1.不能识别日期类型
2.JsonResponse默认要求数据必须是字典，json.dumps中没有此要求
```



```python
import json
@emp.route("/all",methods=['get'])
def query_all():
    users = User.query.all()  #[User,User,User]
    User.query.filter(User.id>12).all() #[User,User,User]
    db.session.query(User.id,User.age,User.birth).all() #((1,18,日期),(2,19，日期),(...))
    def xx(a):
        if isinstance(a,User):
            return {"id":a.id,"age":a.age}
    return  json.dumps(users,default=xx)  # content-type = "text/html"
    或者
    #response = make_response(json.dumps(users,default=xx))
    #response.headers['content-type'] = 'application/json;charset=utf-8'
    #return response
    
    $.ajax({
        type:"get/post",
        url:".....",
        data:"xxx=xxx&xxx=xxx",
        #dataType:"json",  #如果响应头中有 content-type="application/json"，则此参数可省略
        success:function(a){...} #a=xhr.responseText 或 解析后javascript对象
    })
    
    #django中如果使用  JsonRespon响应json，$.ajax中的dataType也是可以省略的
```

```python
from flask import jsonify  #（了解）
@emp.route("/all",methods=['get'])
def query_all():
    #自动设置了响应头：content-type=application/json
    return jsonify(id=1,name="zhj") #响应：'{"id":1,"name":"zhj"}'
    #或者：return jsonify({"id":1,"name":"zhj"}) #{"id":1,"name":"zhj"}
```

> jsonify只能识别简单数据,对于User,Order类型的数据是不能识别的，并且没有提供任何转换接口。

## 蓝图

> 如果所有的view都在一个py文件中，会不利于管理；将不同模块（用户模块，订单模块..）单独起来

> 模块化：类似于django中的app
>
> 1.保证不同模块有自己的路由
>
> 2.有效隔离不同模块（url_prefix）
 ````python
 每个项目模块都可以有自己的view,每个View中都要有自己的蓝图：
 from flask import Blueprint
 mybp = Blueprint("user",__name__,url_prefix='/user') #"user":蓝图名   url_prefix=访问前缀
 
 @mybp.route('/abc/<id>/',methods=['get','post'])  #/user/abc/12/
 def test(id):
 	xxxxxx
 #注意：使用蓝图设置的路由是未激活状态，暂时不能处理请求
 ````

 ```python
#导入蓝图
from user import mybp
app = Flask(__name__)
#注册蓝图
app.register_blueprin(mybp)#注册蓝图，如此蓝图才是活动状态(技巧：注册放在db的构建之后)
 ```

> ### **注意：蓝图有自己的反向解析前缀：**
>
> ### **{{url_for(“user.test”)}}      url_for("user.test")，前缀即为蓝图名**

## 项目结构

 ![structure1](flask-pic\structure1.png)

  ![structure2](flask-pic\structure2.png)

  

> * 在project的根目录下创建目录app，容纳各个项目模块(admin/employee)
> * 每个模块定义自己的蓝图,View,Model
> * 在app目录的init文件中初始化Flask环境 : 如Flask对象和SQLAlchemy对象和Session对象
> * **app目录成为template和static的root_path，所以将static和templates目录放在app目录下**
> * run.py作为启动文件，负责：注册蓝图 和 `app.run()` 


```python
配置信息汇总：
SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost/db116"
SQLALCHEMY_TRACK_MODIFICATIONS = False

#客户端cookie 中 需要的密钥
SECRET_KEY = b'Y\x95IV\x06?-\xa9\xec\x14%\x01o\xf5q\x00\xc2oS\x14'

#mysql-session 需要的配置
SESSION_TYPE = "sqlalchemy"  # session存储类型
SESSION_SQLALCHEMY = db  # SQLAlchemy对象
SESSION_SQLALCHEMY_TABLE = 'sessions'
SESSION_PERMANENT = False  # 浏览器关闭session失效
# 如果会话一直没有活动，30分钟sesison失效，仅适用于SESSION_PERMANENT=True时
# PERMANENT_SESSION_LIFETIME=60*30
SESSION_USE_SIGNER = False  # 是否需要加密cookie
SESSION_KEY_PREFIX = "zhj:"  # sessionID的前缀

#redis-session需要的配置
# SESSION_TYPE = "redis"  # session存储类型
# SESSION_PERMANENT = False  # 浏览器关闭session失效
# # 如果会话一直没有活动，30分钟sesison失效，仅适用于SESSION_PERMANENT=True时
# # PERMANENT_SESSION_LIFETIME=60*30
# SESSION_USE_SIGNER = False  # 是否需要加密cookie
# SESSION_KEY_PREFIX = "zhj:"  # sessionID的前缀
# #redis服务器的链接信息
# SESSION_REDIS = redis.Redis(host='192.168.248.132', port='9007',db=1)
```