from flask_model1 import db133,User
def test1():
    #查询
    users = User.query.all()
    print(users)
def test2():
    #增加
    #1.创建新数据
    user1 = User(name="啊啊啊",age=11)
    user2 = User(name="qqq")
    #2.增加数据
    db133.session.add(user1)
    db133.session.add(user2)
    #3.提交事务
    db133.session.commit()
def test3():
    #删除
    #1.查询要删除的数据
    user = User.query[1]
    #2.删除
    db133.session.delete(user)
    #3.提交事务
    db133.session.commit()
def test4():
    #更新
    user = User.query.filter(User.id==9)[0]
    #2.修改数据的  属性
    user.name="啊啊啊1111"
    user.age=19
    #3.提交事务
    db133.session.commit()
def test5():
    #分页
    page = User.query.paginate(page=1,per_page=3)
    print(page,type(page))
    pages = page.iter_pages()
    print(pages)
    for num in pages:
        print(num)
    print("当前是第",page.page,"页，共",page.pages,"页")
    print(page.items)

def test6():
    #原生sql
    result = db133.session.execute("select id,name,age from t_user133 where id>:id and name like :name",{"id":3,"name":"%c%"})
    print(result,type(result))
    data2 = result.fetchall()
    columns = ("id","name","age")
    data3 = [dict(zip(columns,row)) for row in data2]
    print(data3)
if __name__ == "__main__":
    test5()