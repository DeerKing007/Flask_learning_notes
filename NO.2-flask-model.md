## Model

### ORM：Flask扩展-SQLAlchemy 

> 第三方的ORM框架：**SQLAlchemy**
>
> 基于**SQLAlchemy**进一步定制的**Flask-SQLAlchemy**
>
> `pip install mysqlclient`
>
> `pip install flask-sqlalchemy`

####配置

```python
from flask_sqlalchemy import  SQLAlchemy
#增加mysql配置                                 用户名:密码@ip/数据库名
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:222222@localhost/test"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True #避免警告信息
db9 = SQLAlchemy(app) #构建SQLAlchemy对象 == ORM的核心对象==Flask-SQLAlchemy的核心对象
```

####定义Model类

```python
class User(db9.Model):#基于db构建Model，则Model和数据库建立映射
    __tablename__="user9" #自定义表名，默认为小写类名"user"
    #必须有主键存在
    id = db9.Column(db9.Integer,primary_key=True)#主键，默认自增
    name = db9.Column(db9.String(20),nullable=True,index=True)#默认可为空,建立索引
    age = db9.Column("age9",db9.SmallInteger,unique=True)#唯一，"age9"=列名，默认和字段同名
```

####创建表(类似django的移植)

> 创建完Model后在python-shell中导入db，并调用db.createall()即可创建表

```python
#在项目目录下，执行python，进入python-shell，则项目目录会是sys.path中的根目录之一
>>> from yourapplication import db9  #导入db = SQLAlchemy(app)
>>> from models import User #导入Model
>>> db9.create_all()  #根据Model创建表
>>> db9.drop_all()    #根据Model删除所有表
```

> 注意：也可以自己去建表，只要表名 和 表中的列和Model中的属性，可以一一对应即可

####Model类中的字段类型

> 字段类型

```python
class Test(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column("name2",db.String(20)) #自定义列名
    age = db.Column("age2",db.SmallInteger) #自定义列名
    count = db.Column(db.BigInteger)
    salary = db.Column(db.Float)
    price = db.Column(db.Numeric(5,2))  #decimal
    note = db.Column(db.Text) #存储大量文本
    note_uni = db.Column(db.Unicode(20))
    note_uni2 = db.Column(db.UnicodeText)
    gender= db.Column(db.Boolean)
    birth = db.Column(db.DateTime)
```

```python
CREATE TABLE `test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name2` varchar(20) DEFAULT NULL,
  `age2` smallint(6) DEFAULT NULL,
  `count` bigint(20) DEFAULT NULL,
  `salary` float DEFAULT NULL,
  `price` decimal(5,2) DEFAULT NULL,
  `note` text,
  `note_uni` varchar(20) DEFAULT NULL,
  `note_uni2` text,
  `gender` tinyint(1) DEFAULT NULL,
  `birth` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

####Model类中的字段参数

```python
db.Column(...,primary_key=True)
db.Column(...,unique=True)
db.Column(...,nullalbe=False)
db.Column(...,index=True)
db.Column(...,default=18) #不作用在数据库，在保存数据时，默认值18
db.Column(...,server_default="12.52") #作用在数据库  ，server_default的值必须是字符串格式
db.Column(...,server_default="zhj") #作用在数据库
db.Column(db.DateTime,server_default="2018-12-12")
db.Column(db.TIMESTAMP, server_default=text('now()'))#只有时间戳可以用now设置默认值
```

####Model类中的 表参数

```python
#联合主键：只要为多个列设置primary_key=True即可
class Test(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    id2 = db.Column(db.Integer,primary_key=True)
    ...
    
class Test(db.Model):
    __tablename__ = "自定义表名"
    id = db.Column(db.Integer)
    id2 = db.Column(db.Integer)
    id3 = db.Column(db.Integer)
    id4 = db.Column(db.Integer)
    __table_args__ = (
        UniqueConstraint("id3", "id4"),#联合唯一
        PrimaryKeyConstraint('id', 'id2', name='pks9'),#联合主键
        Index("inds9","id3","id4")#联合索引
    )
```

#### Model的CURD

#####查询所有

```python
User.query #BaseQuery,打印BaseQuery可以输出对应的sql语句
User.query.all() # list of User
```

#####条件查询-- **get**

> 仅用于通过主键查询

```python
User.query.get(1)#select ... where id=1, 返回对象，如果没有数据返回None
User.query.get(2)
```

#####条件查询--**filter_by** 

> 仅用于等值查询，功能有限 （了解）

```python
User.query.filter_by(name="zhj") #BaseQuery
User.query.filter_by(name="zhj",id=1) #BaseQuery ,多个条件是且的关系，id不能用pk代替
User.query.filter_by(name="zhj",id=1).all() #list of User
User.query.filter_by(name="zhj")[0:] #list of User
User.query.filter_by(name="zhj")[:2] #list of User 索引为0 1 没有2
User.query.filter_by(name="zhj")[1:3] #list of User 索引为1 2 没有3
User.query.filter_by(name="zhj")[2] #User对象  索引为2
```

#####条件查询 -- **filter**  （重点）

```python
from sqlalchemy import or_, and_

User.query.filter(User.id == 1,User.name == "zhj") #且  返回BaseQuery
User.query.filter(and_(User.id == 1,User.name == "zhj")) #且 (了解)
User.query.filter(or_(User.id > 1,User.name != "zhj")) #或
User.query.filter(User.id >=1,User.name.like("%z%")) #模糊查询
User.query.filter(User.id.in_((1,2,3)),User.name.like("%z%")) # in in_(tuple)
User.query.filter(~User.id.in_((1,2,3)),~User.name.like("%z%")) #非
User.query.filter(User.id.between(1,4),User.name.like("%z%")) #between 1 and 4 ==[1,4]
User.query.filter(User.name != None) # is not null
id=1;name="%zhj%" #查询条件的表达式中的 右值 可以使用变量
User.query.filter(User.id == id,User.name.like(name))
```

> .query和 .filter返回的都是BaseQuery,可以进步一获取具体数据

```python
User.query.filter(...).all() #返回list of User
User.query.filter(...).one_or_none() #返回一个User或None，如果有多个User报错
User.query.filter(...).one() #返回一个User，如果有多个User或没有 报错
User.query.filter(...).count() #BaseQuery.count() 计数
User.query.filter(...)[0:2] #返回list of User
User.query.filter(...)[1:] #返回list of User
User.query.filter(...)[:2] #返回list of User
User.query.filter(...)[1] #返回User
```

#####映射查询

> 查询部分列

```python
#不能通过User.query..而是通过db.session.query(..)
#SELECT user.id AS user_id, user.name AS user_name FROM user
db.session.query(User.id,User.name) #返回BaseQuery
db.session.query(User.id,User.name).all() #返回所有数据
#SELECT user.id AS user_id, user.name AS user_name FROM user WHERE user.id > %s 
db.session.query(User.id,User.name).filter(User.id > 1) #返回BaseQuery
#[(7, None), (5, ''), (3, 'aa'), (4, 'zhj'), (6, 'zhj')]
db.session.query(User.id,User.name).filter(User.id > 1).all() #返回 list of tuple 不再是Model
#[(7, None), (5, '')]
db.session.query(User.id,User.name).filter(User.id > 1)[0:2] #返回 list of tuple

#补充：
db.session.query(User) #返回BaseQuery  等价于User.query
db.session.query(User).all() #list of User  等价于User.query.all()
db.session.query(User)[1:3] #list of User   等价于User.query[1:3]
```

#####排序

```python
from sqlalchemy import desc, asc
#如下通过db.session.query 或 Model.query都可以。两者等价
#升序排列
#select * from xx order by age asc
User.query.order_by(User.age)
#select id,name from xx order by age asc
db.session.query(User.id,User.name).order_by(User.age) # select id,name from xx order by age asc
#降序排列
#select * from xx order by age desc
User.query.order_by(desc(User.age)) 
#select * from xx where id>1 of name!="zhj" order by age desc
User.query.filter(or_(User.id > 1,User.name != "zhj")).order_by(desc(User.age))
#select id,name from xx where name!="zhj" order by age desc
db.session.query(User.id,User.name).filter(User.name != "zhj")).order_by(desc(User.age))

#联合排序
User.query.filter(or_(User.id > 1,User.name != "zhj")).order_by(User.name,User.id)
#select .. from .. where id>1 or name!="zhj" order by name asc,id desc
User.query.filter(or_(User.id > 1,User.name != "zhj")).order_by(asc(User.name),desc(User.id))
```

#####聚合

```python
from sqlalchemy import func
db.session.query(func.sum(User.id),
                 func.min(User.name),
                 func.avg(User.age),
                 func.max(User.id),
                 func.count(User.id)) #返回BaseQuery
```

#####分组

```python
#select sum(id),name from xx group by name;
db.session.query(func.sum(User.id),User.name).group_by(User.name) #返回BaseQuery
#select sum(id),name from xx group by name having avg(age) in(19,20);
db.session.query(func.sum(User.id),User.name).group_by(User.name)
                                              .having(func.avg(User.age).in_((19,20)))
db.session.query(func.sum(User.id),User.name).group_by(User.name)
                                              .having(func.avg(User.age)==20) #返回BaseQuery
```

> **至此，单表查询，各子句：**
>
> **select** xxx,xxx **from** xxx **where** xxxx  **group** xxx  **having** xx  **order by** xxx desc/asc; **完毕！**

#####增删改

> **需要控制事务**

```python
更新：
user = User.query.get(1)
user.age=11
#db.session.add(user) #可省略
#控制事务
#db.session.rollback()
db.session.commit() #脏数据检测：dirty-check

删除：
user = User.query[1]
db.session.delete(user)
#事务控制
#db.session.rollback()
db.session.commit()

增加：
user = User(name="zhj",age=22)
user2 = User(name="zhjj",age=23)
db.session.add(user)
#db.session.add_all([user,user2])#添加多个
db.session.commit()#提交
#db.session.rollback()#回滚
```
#####分页

```python
#select ... order by id desc limit 0,3
User.query.order_by(desc(User.id)).limit(3).offset(0) #了解

#SQLAlchemy支持
s = User.query.paginate(page=1,per_page=2) #查询第一页，每页显示2条,返回一个Pagination对象
print(s.iter_pages()) #页号的序列[1,2,3,4]
print(s.query) #查询用的sql语句
print(s.page)#当前页号
print(s.per_page) #每页几行
print(s.total)#共多少行
print(s.pages)#共多少页
print(s.items) #当前页的数据
print(s.prev_num) #上一页号
print(s.next_num)
print(s.has_next) #是否有下一页
print(s.has_prev)

#注意，以后可以直接将s传给template
```

#####raw-sql

> 如果上述支持不足够满足需求，原生sql

```python
#执行原生sql                                  sql语句                                 sql中的参数
result = db.session.execute("select max(id) as m,min(id) as i from user where id>:aa",{"aa":1})
result.fetchone() #tuple 获取一条数据
result.fetchmany(2) #List of tuple  获取2条数据
result.fetchall() #list of tuple 获取所有数据
```

####Model中的关联关系

#####一对多关系

```python
class User(db.Model):
    __tablename__="user99"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    #relationship用于搭建关系，声明关系属性，关系对方是Order，且对方为1：*中的*
    orders = db.relationship("Order",backref="user9",lazy="dynamic")
class Order(db.Model):
    __tablename__="order99"
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    #在从表方，定义外键列，并明确指定主键位置：user99.id
    user_id = db.Column(db.Integer, db.ForeignKey('user99.id')) #user99.id=表名.列名
```

```python
#双方同时增加
user = User(name="aaa")
order = Order(price="10000")
order2 = Order(price="20000")
order3 = Order(price="30000")
user.orders.append(order) #维护关系
user.orders.append(order2) #维护关系
db.session.add(user) #增加（级联增加==User增加时级联的增加了关系对方Order）
db.session.commit()

#增加一方
user = User.query.get(1) #持久化对象（在数据库中有对应数据，且在session的检测下）
order = Order(price="40000") #临时对象(在数据库没有对应数据，)
order.user9=user #搭建关系（user9时主表方的backref="user9"）
db.session.add(order)
db.session.commit()
或者
order = Order(price=10000)
user = User.query.get(1) #持久化对象，此对象在事务提交时会有dirty-check
#搭建关系
user.orders.append(order)
db.session.commit()

#修改（略）
#删除
user = User.query.get(1)
db.session.delete(user)
db.session.commit() #用户1相关的order的外键被置null
```

> 补充： orders = db.relationship("Order",...，**cascade="save-update，delete"**)
>
> #### **主操作时，可以对从有级联行为**
>
> **cacade=“all/save-update/delete”**  **#save-update为默认**
>
> **save-update :** 在增加和修改主时，级联增加修改从
>
> **delete :** 在删除主时，级联删除从 (慎用)
>
> **all :** 所有级联行为

```python
#查询:查询一方，可级联到另一方
####################### 通过一获取多 #################################
users = User.query #BaseQuery
users.all() #list of User
users[0] #User

orders = users[0].orders #AppenderBaseQuery，得到Query对象
orders.all() #查询当前用于的order
#此处在查询关系一方时，对于关系对方会延迟查询(lazy-load)

####################### 通过多获取一 ################################
orders_query = Order.query #BaseQuery
orders = Order.query.all() #list of Order
orders[0].user9 #User,此时查询对应订单的用户，得到User对象
```

```python
#隐式表连接 (了解)
#SELECT 
#	user99.id AS user99_id, user99.name AS user99_name 
#FROM 
#	user99, order99 
#WHERE 
#	user99.id = order99.person_id AND order99.id > 1
User.query.filter(User.id == Order.user_id,Order.price>100) #查询订单价格大于100的用户
#注意：此时，依然是只查询了一方，只是用对方做了where条件

Order.query.filter(User.id==Order.user_id,User.name.like("%z%")) #查询名字包含z的用户的订单
```

```python
#表连接,只查询一方
Order.query.join(User) #返回BaseQuery,只查询Order数据
User.query.join(Order) #返回BaseQuery,只查询User数据
User.query.join(Order).filter(User.id>10,Order.price>200) #BaseQuery
User.query.outerjoin(Order).filter(User.id>10,Order.price>200).all() #返回list of User

#表连接，查询双方
db.session.query(User,Order).outerjoin(Order) #外连接  User outerjoin Order
db.session.query(Order,User).join(User) #内连接  Order join User
#[(<User 2>, <Order 1>), (<User 1>, <Order 2>)]
db.session.query(User,Order).outerjoin(Order).all() #返回list of tuple
db.session.query(User,Order).outerjoin(Order).filter(....).all() #返回list of tuple

#多表连接
db.session.query(User,Order,Address).join(Order).join(Address)
User.query.join(Order).join(Address)
```

> **lazy选项**
>
> 'select' (默认值) 就是说 SQLAlchemy 会使用一个标准的 select 语句必要时一次加载数据。
>
> 'joined' 告诉 SQLAlchemy 使用 JOIN 语句作为父级在同一查询中来加载关系。
>
> 'subquery' 类似 'joined' ，但是 SQLAlchemy 会使用子查询。
>
> 'dynamic' 在有多条数据的时候是特别有用的。不是直接加载这些数据，SQLAlchemy 会返回一个查询对象， 
>
> ​                 在加载数据前您可以过滤（提取）它们。
>
> **实例：**
>
> user = User.query
>
> order = user[0].orders
>
> **select** : User.query时只查询User ; order是list of Order     
>
> **joined**：User.query时通过join连接查询双方 (查询时，负载过重)
>
> **dynamic**:User.query时只查询User ; order是BaseQuery **(建议使用的懒加载模式)**    

> **注意：lazy选项只适用于一对多中主表方，和多对多双方**

#####多对多关系

```python
tags = db.Table("t_student_course",#表名
               db.Column("student_id",db.Integer,db.ForeignKey("students.id"),primary_key=True),
               db.Column("course_id", db.Integer,db.ForeignKey("courses.id"),primary_key=True)
)
class Student(db.Model):
    __tablename__="students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),unique=True)
    #关系属性：1.声明关联关系   2.操作数据时可以获取对方数据，可以关联查询对方
    courses = db.relationship("Course",secondary=tags,backref="stus",lazy="dynamic")
    #stuent加载course是懒加载，course加载student时也是懒加载。懒加载只能给一对多的主表和多对多的双方
    #courses = db.relationship("Course", secondary=tags,        
    #                           backref=db.backref("stus",lazy="dynamic"), lazy="dynamic")
class Course(db.Model):
    __tablename__="courses"
    id = db.Column(db.Integer, primary_key=True)
    expire = db.Column(db.SmallInteger)
```

```python
#连接查询
Student.query.join(Student.courses).filter(Course.expire>10)
db.session.query(Student).join(Student.courses)  #只查询了Student

Course.query.join("stus").filter(Student.id>10)#只查询了Course
db.session.query(Course).join("stus").filter(Course.expire>10,Student.id<20)

db.session.query(Student,Course).join(Student.courses)#保留双方数据
#查一方
courses = Course.query.all() #list of Student
course_query = courses[0].stus #通过backref获取对方，（ops:由于是懒加载，只返回一个BaseQuery）
                               #(1:*  user=User.query.get(1); user.orders)
course_query.all() # list of Course
#增加双方数据
cour = Course(expire=100)
stu = Student(name="zhj31")
cour.stus.append(stu)#维护关系：将学生交给课程
db.session.add(cour)#添加课程（ops:会级联添加持有的所有学生）
db.session.commit()
#增加双方数据
cour = Course(expire=101)
stu = Student(name="zhj32")
stu.courses.append(cour)#维护关系：将课程交给学生
db.session.add(stu) #添加学生(ops：会级联的添加所有持有的课程)
db.session.commit()
#增加一方数据
cour = Course.query.get(12)
stu = Student(name="zhj33")
stu.courses.append(cour) #维护关系：将课程交给了学生
db.session.add(stu) #添加学生（ops:通过持有的课程，获得外键）
db.session.commit()
#增加一方数据
cour = Course.query.get(12)
stu = Student(name="zhj33")
cour.stus.append(stu) #维护关系：将学生交给了课程
db.session.commit()# 由于cour是持久化对象，所以会有dirty-check,会添加学生
#删除
cour = Course.query.get(12)
db.session.delete(cour) #会自动置空外键
db.session.commit()
#更新(略)
```

##### 一对一关系

```python
class Person(db.Model):
    __tablename__="person"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    #uselist=False 关系不是1：* 而是1:1  （ops:在1:*中uselist取默认值True）
    passport = db.relationship("Passport",uselist=False,backref="person")
class Passport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(20))
    #person.id = 表名.列名
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),unique=True)
```

```python
#增加双方
per = Person(name="aaa")
passport = Passport(note="zzz")
per.passport=passport
db.session.add(per)
#passport.person=per
#db.session.add(passport)
db.session.commit()

#增加一方
per = Person.query.get(1) #持久化对象
passport = Passport(note="zzz")
per.passport=passport #维护关系：将passport交给person
#db.session.add(per)
db.session.commit() #持有关系的持久化对象per，会在dirty-check时，增加passport

#更新（略）

#删除
per = Person.query.get(1)
db.session.delete(per)
db.session.commit() #从表外键置空，如果要讲从表数据一起删除，需要设置cascade

#查询
person = Person.query.get(1)
passport = person.passport #获取对方（没有懒加载）

person = Person.query.join(Passport) #表连接
passport = person[0].passport #获取对方
db.session.query(Person,Passport).join(Passport)#表连接，留双方数据
```