Vacseen
===

<p align="center">
  <img src="static/image/logo.png">
</p>

[![Build Status](https://travis-ci.com/llleyelll/vacseen.svg?token=Vf6PJtHdqGqqThMwgTem&branch=master)](https://travis-ci.com/llleyelll/vacseen)


**Vacseen** is an online tracker that gives user help related to basic vaccines such as type of vaccine, suggestions according to user's gender and age such as that a 1-month old newborn baby needs to take the second dose of Hepatitis B. And also notifies the user if he/she needs to get the vaccine again. It is accessible anywhere and anytime through the “Internet”, which is surely more convenient than carrying or finding a vaccine book.

Prerequisite
---
- Python 3.7+
- Django 2.2.7
- Google OAuth API

Get started (run locally)
---
1. Clone the repository and change directory to `vacseen` directory.
```
$ git clone https://github.com/llleyelll/vacseen.git && cd vacseen/
```
2. Create `.env` file for python decouple. In `.env` file should have these following.
```
DEBUG=True
SECRET_KEY=YOURSECRETKEY
TIME_ZONE=Asia/Bangkok
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=YOURGOOLEAPIKEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=YOURGOOLEAPISECRETKEY
SOCIAL_AUTH_POSTGRES_JSONFIELD=True
```
3. Create virtualenv in the directory and activate virtualenv.
```
$ virtualenv venv
$ source venv/bin/activate
```
4. Install all dependencies and then run database migrations by the following commands.
```
(venv) pip install -r requirements.txt
(venv) python manage.py migrate
```
5. Create superuser
```
(venv) python manage.py createsuperuser
``` 
6. Add and configure Google credential in `http://127.0.0.1:8000/` using `python manage.py runserver` to start a server. Go to `http://127.0.0.1:8000//admin` to configure Google credential by setting sites and social applications table. While setting social applications add Client id and Secret key and add your created site to available sites.

Team Members
---

| Name                      | Roles                    | GitHub                                        |
|---------------------------|--------------------------|-----------------------------------------------|
| Chanachida Fuachai        | Developer                | [llleyelll](https://github.com/llleyelll)     |
| Sirikorn Songsaengthong   | Developer                | [Sirikonss](https://github.com/Sirikonss)     |
| Sivanat Subpaisarn        | Developer                | [tiemfah](https://github.com/tiemfah)         |

Project Documents
---
- Mockup - [Google Drive](https://drive.google.com/drive/u/2/folders/17v6zQXK7f5lJ0oV4sSBYkhxH5CGzu6ub)
- Task Board – [Trello](https://trello.com/b/o1FQrdfy)
- Issue Tracker – [Github Issues](https://github.com/llleyelll/vacseen/issues)
- Iteration Plan – [Google Doc](https://docs.google.com/document/d/17WCf1Z5uMvR2h9EOO3qqsbqW-7lzxDNflHzLacBrkoA/edit?usp=sharing)
- Iteration Script – [Google Doc](https://docs.google.com/document/d/1paqaK2TXelRTuHvvccfSNGVF_0o_pkhiHLibLo6QdT0/edit?usp=sharing)
- Code Review Checklist – [Google Doc](https://docs.google.com/document/d/1sJqZ3WlXeycAEXh6zB1JEkJHjNAY0ihp8oIT0eFlDfk/edit?usp=sharing)
- Code Review Script – [Google Doc](https://docs.google.com/document/d/1YScK9uWoZnyaVXmA61DaatdICU6vgYCh_Xi2Ky7ckfA/edit?usp=sharing)
