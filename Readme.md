## TigerHack 2018

---

在什么地方比同级产品强？
正文对资源的正反向反馈

实际上这些图片很多是记者自己拍的
使用统一的接口即可

大文本框[媒体工作者编辑器]
搜索框_文本[]
搜索框_语音[]

{
main_text -> String
search_text -> String
}

-> 
数组 Card

开启 CORS


# for gunicorn in *unix
#    from werkzeug.contrib.fixers import ProxyFix
#    app.wsgi_app = ProxyFix(app.wsgi_app)


'''
conn = connect('test', host='mongodb://10.7.109.196/test')

class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)


class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)
    meta = {'allow_inheritance': True}


class TextPost(Post):
    content = StringField()
'''

'''
@app.route('/user')
def test_user():
    user_1 = User()
    user_1.email = "hd945@maill.missouri.edu"
    user_1.first_name = "Ding"
    user_1.last_name = "Hao"
    user_1.save()
    return "Test User"


@app.route('/users')
def test_get_users():
    for i in User.objects:

'''

Key Phrase Extraction API使用Key Phrases方法从文本文档中提取关键短语。

pip install -U flask-cors

CORS
@cross_origin()

# gunicorn -w 4 -b 127.0.0.1:8000 入口文件名:app
# pip freeze > requirements.txt
# https://www.jianshu.com/p/9ede1f0854a1
# https://juejin.im/post/5a5c1825f265da3e3e33bf70