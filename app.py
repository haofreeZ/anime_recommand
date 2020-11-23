#coding=utf-8
# 导入Flask类
from flask import Flask, render_template, request
from recommand import recommand

# Flask类接收一个参数__name__
app = Flask(__name__)


# 装饰器的作用是将路由映射到视图函数index
@app.route('/')
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    # user_id = request.args.get("user_id")
    user_id = 1
    data = recommand(user_id)
    return render_template("search.html", data=data)


# Flask应用程序实例的run方法启动WEB服务器
if __name__ == '__main__':
    app.run(debug=True)
