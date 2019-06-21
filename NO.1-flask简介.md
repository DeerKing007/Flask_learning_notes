# 	Flask

## 简介

> 微型框架，核心简单，但易于扩展。给开发人员足够的自由。
>
> 默认情况下，Flask 不包含数据库抽象层、表单验证，或是其它任何已有多种库可以胜任的功能。然而，Flask 支持用扩展来给应用添加这些功能，如同是 Flask 本身实现的一样。
>
> Flask 也许是“微小”的，但它已准备好在需求繁杂的生产环境中投入使用

## Flask 安装

`pip install flask`   即可!

## 第一个程序

```python
from flask import Flask

app = Flask(__name__) #初始化application实例，将成为核心对象，负责管理整个应用，处理所有请求。view， 
                      #urlConf等等都要注册于Flask对象。
    

@app.route('/')  #为view方法提供路由。即通过 “/” 可以访问
def hello_world():
    #a=10/0 #如果是调试模式开启，可以看到详细的错误信息
    return 'Hello World!' #返回值即为响应内容，将显示在用户的浏览器上


if __name__ == '__main__':
    #app.run()  #启动内置的web服务器，启动后即可接受外界用户的访问了
    app.run(debug=True,host="localhost",port=9000) #定制细节
    #注意：开启了调试模式后，当程序出错时，可以在浏览器看到更详尽的信息
```

## urlConf

```python

@app.route('/') # /可以访问
def hello_world():
    a = 10 / 0
    return 'Hello World!'

@app.route('/a/b/') #/a/b/可以访问
def hello_world():
    a = 10 / 0
    return 'Hello World!'

@app.route("/a/<name>/") #命名路径
def test(name):
    print("name:", name)
    return "hh"
```

###转换器

> **对于命名路径,可以使用转换器，限定内容**

```python
"""
内置转换器:
      名称                  实现类
    'default'        UnicodeConverter,
    'string'         UnicodeConverter,
    'any'            AnyConverter,
    'path'           PathConverter,允许出现‘/’
    'int'            IntegerConverter,接收整数
    'float'          FloatConverter,接收浮点数
    'uuid'           UUIDConverter
"""

@app.route("/b/<int:age>/") #只接受整数，test2中age参数类型为int，不再是默认的string
def test2(age):
    print("age:", age, type(age))
    return "hh"

@app.route("/a/<string:name>/") #string 可以不用定义，默认就是接收字符串 (了解)
def test1(name):
    print("name:", name)
    return "hh"

@app.route("/c/<any('zhj','abc'):name>/") # /c/zhj/ 或 /c/abc/可以访问,name="zhj"或"abc"(了解)
def test3(name):
    print(name)
    return "hh"

@app.route("/d/<path:name>/") # /d/a/b/c/d/ 可以访问，name="/a/b/c/d"(了解)
def test4(name):
    print(name)
    return "hh"

@app.route("/e/<uuid:name>") # /e/b9630970-27af-4da9-929b-20daaf2af959可以访问(了解)
def test5(name):
    print(name)
    return "hh"
```

###自定义正则转换器

```python
#1.正则转换器
class RegexConverter(BaseConverter): #自定义类，继承BaseConverter(所有转换器的父类)
    def __init__(self, map, *args):#args=转换器的参数
        self.map = map
        self.regex = args[0]  #BaseConberter中的属性regex
#2.注册转换器              名称           实现类
app.url_map.converters['regex9'] = RegexConverter #注册自定义转换器

#3.使用转换器：regex9
@app.route('/docs/model_utils/<regex9("[a-z]{3}"):name>') # "[a-z]{3}"会传递给实现类的args
def hello(name):
    ....
```



##跳转

####View 到 View

```python
@app.route("/xx/xx/")
def xx():
    print("....")
    #return redirect("/a/b/c/") #重定向到/a/b/c/

@app.route("/a/b/c/")
def test5():
    print("...")
    ...
```

####View 到 Template

```python
def xx():
    ...
    return render_template("test.html") #转发到test.html (ops:模板根目录是 templates)
```

####反向解析

```python
View中：return redirect(url_for("test5")) #url_for反向解析url  url_for(“view函数名”)
Template中：<a href="{{ url_for('test5') }}">test5</a> 

```



## 请求参数接收
###Get请求参数

```python
from flask import request
request.args.get("id") #获取id参数,没值报None
request.args["id"] #获取id参数,没值报错
request.args.getlist("id") #返回list
```

### Post请求参数

```python
from flask import request
request.form.get("id") #获取id参数,没值报None
request.form["id"] #获取id参数,没值报错
request.form.getlist("id") #返回list 
```


> **注意：View函数默认直接收Get请求，如果要发送post，需要设置：**
>
> ```python
> @app.route("/flask/param2/",methods=['GET', 'POST']) #允许get请求和post请求
> def xx():
> 	....
> ```

##技巧：重定向传值

```python
return redirect(url_for('test1',name="aaaaa")) #重定向中利用命名路径传值

@app.route("/xxx/xx/<name>")
def test1(name):
	....
```

```python
return redirect("/flask/page/?id=1") #重定向中携带请求参数(ops:没有做反向解析)

@app.route("/flask/page/")
def xxx():
	request.args.get("id")
	...
```

```python
session传值...
```
## 模板使用-Jinja2

### 基本使用

> http://docs.jinkan.org/docs/jinja2/templates.html --中文文档

> flask 已经内置了模板语言：Jinja2
>
> 注意：flask项目的模板根目录是：`项目根目录下的templates目录`

> 转发模板：

```python
from flask import render_template
return render_template("test.html")
return render_template("bk9/test.html")
```

### 传递数据-传值

> 向模板中传递数据
>
> 如下，传递数据：age=18 , gender=True , data={"name":"zhj","hobby":["ft","bb"]}

```python
return render_template("bk9/test.html",
                       age=18,gender=True,data={"name":"zhj","hobby":["ft","bb"]}
                      )
```
###获取数据-取值

> 模板中获取数据 {{ key }} 

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    this is test {{ age }}  -- 
                 {{ gender }} -- 
                 {{ data.name }} --
                 {{ data.hobby }} --
                 {{ data.hobby[0] }} --
	{# <input type="text" name="id"/> 单行注释#}
    {# <input type="text" name="id"/>
       <input type="submit" value="提交"/> 多行注释#}
</body>
</html>
```

####过滤器

> 内置过滤器

```python
{{ data.list|length }}
{{ data.name|upper }}
{{ data.name|upper|lower|trim }} <!-- trim消除头尾的空格 -->

{{ a |default("zzz") }} <!-- 如果View没有向Template传递a，则显示默认值"zzz" -->
{{ a |default("zzz"，true) }} <!-- 如果a的值为None、0、False、“” 则显示默认值"zzz" -->
```

> 过滤器补充 : 日期数据格式化

```python
#定义过滤器函数
def dateformat9(value, format="%Y-%m"):#format的默认值是可选的
    return value.strftime(format)

#在Flask实例app中注册自定义的过滤器：名为"date9"
app.jinja_env.filters['date9']=dateformat9
```

```jinja2
在模板中对birth进行格式化处理：使用自定义的过滤器
{{ birth|date9('%Y-%m-%d %H:%M:%S') }}
```

####测试器

> `is 测试器`
>
> 进行各种判断

```python
测试器：defined=是否有值
{% if birth is defined %} 
	birth is there
{% endif %}
{% if birth %}
	birth is there2
{% endif %}

测试器：divisibleby=是否可以整除
{% if data.list.0 + 1 is divisibleby(2) %}
	{{ data.list.0 }} % 2 == 0
{% endif %}
{% if not data.list.0 + 1 is divisibleby(2) %}
	{{ data.list.0 }}  not % 2
{% endif %}

测试器：lower/upper=是否是小写/大写字符
{% if data.name is lower %} {# upper 是大写#}
	name is lower
{% endif %}
        
测试器：even/odd=是否是偶数/奇数
{% if not data.list.0 + 1 is even %} {# odd 是奇数测试#}
	1+1 是偶数
{% endif %}
```

#### 运算

```
{{ data.list.0 + 1 }}
{{ data.list.1 - 1 }}
{{ data.list[0] * 10 }}
{{ data.list[0] / 2 }}
{{ (data.list[0] + 1) % 2 }}

{{ data.list[0]>1}}
{{ data.list[0]==1}}
{{ data.list[0]<=1}}
{{ data.list[0]!=1}}

{{ data.list[0]==1 and 1==2 or 1==1}}
{{ data.list[0]==1 and 1==2 or not 1==1}}

{{ "hilo" ~ data.name ~ "!!" }} {# 字符串拼接 #}
```

### 模板中逻辑处理

* 逻辑判断 : 0、None、“”、[]、没值  都做为False

```python
{% if data.list|length < 10 %}
	lt 10
{% endif %}

{% if age + 1 < 10 %}
	lt 10
{% endif %}

{% if age + 1 > 17 and name|trim=="zhj" and name is lower %}
	.....
{% endif %}

{% if data.name|trim == "zhj" %}
	hilo,zhj
{% endif %}

{% if data.name == "zhj" %}
	hilo,zhj
{% elif not data.name|trim=="zhj" %}
	hilo,zhj2
{% else %}
	hilo,zhj3
{% endif %}
```

* 循环遍历

```python
{% for user in users %}
  <li>{{ user.username }}</li>
{% endfor %}

{% for user in users %}
    {% if loop.index is odd %}
    	<li><span style="color:red">{{ user.username }}</span></li>
    {% elif loop.index is even %}
    	<li><span style="color:green">{{ user.username }}</span></li>
    {% endif %}
{% endfor %}

{% for key, value in my_dict.items() %}
    {{ key }}
    {{ value }}
{% endfor %}

range()--模板的全局函数 range(4) == range(0,4) == range(0,4,1) == [0,1,2,3]
{% for number in range(10) %}
    <a href="xxxx?num={{number}}">{{number}}</a>
{% endfor %}
```

###模板继承

> 在多个模板文件中，会有相同的部分，造成模板代码冗余
>
> 通过父模板的定义，抽取出所有的冗余部分。
>
> 利于维护

```python
base.html
...
<body>
    <div style="background-color:lavender;margin-bottom: 100px">
        欢迎你，{{ user.name }}
    </div>
    {% block content%}
    {% endblock %}
    <div style="font-size: 12px;color:#999;margin:0 auto;text-align: center;padding:20px 0">
        Copyright © 2013-2018
        <strong><a href="#" target="_blank">百知</a></strong>&nbsp;
        <strong><a href="#" target="_blank">baizhi.com</a></strong> All Rights Reserved. 
    </div>
</body>
```

```python
sub.html
{% extends "base.html" %}
{% block content %} {!-- 覆写父模板block --}
    <div style="height: 100px;background-color: #999999">
        这是子类模板自己的内容
    </div>
    {%block xx%}
    {%endbolock%}
{% endblock %}

```

###模板包含

> 可以将一个大页面先做好布局，然后布局内的内容可以单独定义一个模板文件，然后在做包含
>
> 便于管理复杂的模板文件
>
> 效果和ajax中的load方法相似

```html
...
<body>
    <div style="float: left;height: 300px;width:200px">
        {% include "part1.html" %}
    </div>
    <div style="float: left;height: 300px;width:200px">
        {% include "part2.html" %}
    </div>
</body>
...
```

```html
part1.html:可以是一个完整的html，也可以是html片段
<div style="width: 100px;height: 300px;background-color: red">{{ birth }}</div>
```

> 注意：include和ajax的load方法区别：
>
> include标签：{%include%}在服务器运行，在一个请求内运行
>
> ​                     ：include很多，或导致请求偏重
>
> ajax:load：是在浏览器运行，会触发多次请求
>
> ​                 ：load很多，或导致请求次数偏多

## 全局错误页面

> 错误提示

```python
@app.errorhandler(404) #404错误会自动转到此view，这样就单独定制了404页面
def not_found(e):
	return render_template("404.html")

@app.errorhandler(500) #500错误会自动转到此view，这样就单独定制了500页面(非调试模式下有效)
def not_found(e):
	return render_template("500.html")
```