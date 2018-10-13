## TigerHack 2018

---

当前媒体工作者在工作中会遇到各式各样的问题
典型的问题有几种

1. 对于非自己领域的事物的认知困难 （从而对采访对象提出的问题不合时宜或者是在写新闻稿的时候十分门外汉）
典型例子是前几周的新闻“黎曼猜想 阿蒂亚”
很多新闻工作者对“黎曼猜想” 或者 “阿蒂亚” 这个人并没有足够的知识（哪怕是最浅显的）


实际上上面的几点问题都可以概括为没有工具链（技术栈）以及工具链没有得到良好的配置

1. 没有工具链
试想一下，如果直到今天程序员们还在使用notepad编程，
那么编程的效率将会受到多大的影响。 :(

2. 工具链没有得到良好的配置
类似于 Java Spring Boot还没有诞生的时候
大家都在使用 xml 配置来编程
对于前端而言，这种自动配置起到了项目模板的作用
（https://github.com/facebook/create-react-app）

我们相信媒体工作者正面临着多年前程序员们曾经面临着的困境
 

---

功能：

1. 类似的报道

事件，地理，时间

2. 录音搜索

在什么地方比同级产品强？
正文对资源的正反向反馈
摆脱搜索引擎的请求字数限制


正文字段 -> 生成函数
搜索字段 -> 抑制/激发函数

但是不可否认的是对于很多新闻工作者
对于第一手报道，他们很少会使用网络上流传的图片
更多的是来自自己公司的资源与自己拍摄的图片
但是这些图片实际上可以表示更高维度的知识
我们的作品可以导入图片完成从图片找到相关的新闻的功能



实际上这些图片很多是记者自己拍的
使用统一的接口即可

这些图片或者文字也往往隐含了地理信息

通过这些地理信息再找到和这个地区相关的信息



大文本框[媒体工作者编辑器]
搜索框_文本[]
搜索框_语音[]

{
main_text -> String
search_text -> String
} 

结果一：
图片
和图片相关的url

结果二：
实体 -> 地名，名词


-> 
数组 Card

# for gunicorn in *unix
#    from werkzeug.contrib.fixers import ProxyFix
#    app.wsgi_app = ProxyFix(app.wsgi_app)

Key Phrase Extraction API使用Key Phrases方法从文本文档中提取关键短语。

pip install -U flask-cors

CORS
@cross_origin()


## install 



# gunicorn -w 4 -b 127.0.0.1:8000 入口文件名:app
# pip freeze > requirements.txt
# https://www.jianshu.com/p/9ede1f0854a1
# https://juejin.im/post/5a5c1825f265da3e3e33bf70