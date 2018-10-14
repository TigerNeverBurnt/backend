## TigerHack 2018

## Team Member

---

- Huiming Sun
- Xinrui Yang
- Han Song
- Ding Hao
- Jianan Ni

---

## Deploy in Ubuntu-18.04

---

```bash
sudo apt-get update
udo apt-get install nginx
sudo apt-get install python3.6
sudo apt-get install python3-pip
sudo pip3 install virtualenv
```

```bash
git clone https://github.com/TigerNeverBurnt/backend.git
cd backend
```

```bash
scp -r <remote>:<Path>/.aws/ ./
scp -r <remote>:<Path>/.azure/ ./
scp -r <remote>:<Path>/.google/ ./
```

```bash
virtualenv venv 
source venv/bin/activate
pip install -r requirements.txt
gunicorn app:app -c gunicorn.conf.py
```

## Operating Parameters

---

- bind = '0.0.0.0:8000'
- backlog = 2048
- pidfile ./app.pid
- worker 5
- ....

You Can Edit `gunicorn.conf.py` to change default config 


## Purpose

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

1. 寻找类似报道

事件，地理，时间

2. 录音搜索

在什么地方比同级产品强？
正文对资源的正反向反馈
摆脱搜索引擎的请求字数限制


正文字段 -> 生成函数
搜索字段 -> 抑制/激发函数

3. 名人识别


4. 地理联系


5. 高亮联想

6. 图片推荐

但是不可否认的是对于很多新闻工作者
对于第一手报道，他们很少会使用网络上流传的图片
更多的是来自自己公司的资源与自己拍摄的图片
但是这些图片实际上可以表示更高维度的知识
我们的作品可以导入图片完成从图片找到相关的新闻的功能

实际上这些图片很多是记者自己拍的
使用统一的接口即可

这些图片或者文字也往往隐含了地理信息

通过这些地理信息再找到和这个地区相关的信息
