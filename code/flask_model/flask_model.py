from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint, Index

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:321654@localhost/db133"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True

db133 = SQLAlchemy(app)
@app.route('/')
def hello_world():
    return 'Hello World!'

class User(db133.Model):
    __tablename__ = "t_user133" #表名
    id = db133.Column("id",db133.Integer,primary_key=True)
    id2 = db133.Column("id2", db133.Integer, primary_key=True)
    name = db133.Column(db133.String(30),unique=True,index=True) #varchar(30)
    name2 = db133.Column(db133.String(20))
    age = db133.Column(db133.SMALLINT,nullable=False,server_default="18")


if __name__ == '__main__':
    app.run()
