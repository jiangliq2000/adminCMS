## 简介
server 是一个使用Python编写的REST API，可以对多个资源提供增删改查服务，用于快速构建REST应用。  
1. Web框架使用Flask
2. ORM框架使用peewee
3. 安全方面使用了flask-jwt插件进行JWT(Json Web Token)认证


## 第三方依赖
- peewee
- pymysql
- Flask
- Flask-JWT

## 环境配置
### venv虚拟环境安装配置
```
sudo pip3 install virtualenv
virtualenv venv
. venv/bin/activate
```

### 指定venv 版本
cd /projectdir
virtualenv -p C:\Python\Python36\python.exe venv36

激活版本：
venv36\Scripts\activate


### 第三方依赖安装
```
pip3 install -r requirements.txt

```
### 系统参数配置
1. 编辑`config.py`， 修改SECRET_KEY及MySQL数据库相关参数
```
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret'
DB_HOST = '127.0.0.1'
```
2. 编辑log-app.conf，修改日志路径
```
args=('logs/apiserver.log','a','utf8')
```


### 启动应用
```
python app.py (仅限测试)

生产环境：
gunicorn -w 4 -b 0.0.0.0:6080 wsgi:application
```


