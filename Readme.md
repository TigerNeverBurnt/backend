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
sudo apt-get install nginx
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

