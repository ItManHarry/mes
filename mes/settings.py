"""
Django settings for mes project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import sys
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# 将Apps放到同一目录下
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
# 系统登录地址,配置后在login_required拦截后会自动跳转至对应的登录页面
LOGIN_URL = '/sys_sign/login/'
# 文件上传地址
UPLOAD_FILE_PATH = 'E:/attachments'
# 分页-每页数据量
PAGE_ITEMS = 10
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v=$3))p1*6co6#t+cwg%_sy)z^2r^#x&53%(!vye+j5s@@l4yx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# 生产环境关闭Debug模式
# DEBUG = False
# ALLOWED_HOSTS = ['*']
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_URL = '/static/'
# 允许iframe显示在app页面中
X_FRAME_OPTIONS = 'ALLOWALL url'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_apscheduler',           # 定时任务插件-APScheduler
    'jobs.apps.JobsConfig',         # 系统定时任务模块
    'api.apps.ApiConfig',           # 对外接口
    'common.apps.CommonConfig',     # 系统公共模块(创建公共表)
    'sys_sign.apps.SysSignConfig',  # 系统登录模块
    'sys_auth.apps.SysAuthConfig',  # 系统权限模块(角色&菜单)
    'sys_dict.apps.SysDictConfig',  # 系统字典
    'org_com.apps.OrgComConfig',    # 组织模块-公司
    'org_dep.apps.OrgDepConfig',    # 组织模块-部门
    'org_emp.apps.OrgEmpConfig',    # 组织模块-雇员
    'pp_master.apps.PpMasterConfig',    # 生产模块-Master数据
    'ld_stock.apps.LdStockConfig',      # 物流模块-出入库管理
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mes.sys.middleware.session_check',
]

ROOT_URLCONF = 'mes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mes.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mes',
        'USER': 'mes',
        'PASSWORD': 'Mes2023$',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# 邮箱配置
EMAIL_HOST = 'hdi-relay.hd.com'
DEFAULT_FROM_EMAIL = 'guoqian.cheng@hd.com'
# 配置Log
from logs.log_path import LOG_DIR
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {     # 格式器
        'verbose': {    # 详细
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'standard': {   # 标准
            'format': '[%(asctime)s] [%(levelname)s] %(message)s'
        },
    },
    # handlers：用来定义具体处理日志的方式，可以定义多种，"default"就是默认方式，"console"就是打印到控制台方式。file是写入到文件的方式，注意使用的class不同
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            # 'stream': 'ext://sys.stdout',   # 文件重定向的配置，将打印到控制台的信息都重定向出去 python manage.py runserver >> /home/aea/log/test.log
            'stream': open(os.path.join(LOG_DIR, 'console.log'), 'a'),              # 虽然成功了，但是并没有将所有内容全部写入文件，目前还不清楚为什么
            'formatter': 'standard'                                                 # 制定输出的格式，注意 在上面的formatters配置里面选择一个，否则会报错
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'mes.log'),       # 这是将普通日志写入到日志文件中的方法，
            'formatter': 'standard'
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'all.log'),       # 日志输出文件
            'maxBytes': 1024*1024*10,                           # 文件大小
            'backupCount': 10,                                  # 备份份数
            'formatter': 'standard',                            # 使用哪种formatters日志格式
        },
        # 上面两种写入日志的方法是有区别的，前者是将控制台下输出的内容全部写入到文件中，这样做的好处就是我们在views代码中的所有print也会写在对应的位置
        # 第二种方法就是将系统内定的内容写入到文件，具体就是请求的地址、错误信息等，小伙伴也可以都使用一下然后查看两个文件的异同。
    },
    'loggers': {  # log记录器，配置之后就会对应的输出日志
        # django 表示就是django本身默认的控制台输出，就是原本在控制台里面输出的内容，在这里的handlers里的file表示写入到上面配置的file-/log/jwt_comment.log文件里面
        # 在这里的handlers里的console表示写入到上面配置的console-/log/console.log文件里面
        'django': {
            'handlers': ['console', 'file'],
            # 这里直接输出到控制台只是请求的路由等系统console，当使用重定向之后会把所有内容输出到log日志
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request ': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',         # 配合上面的将警告log写入到另外一个文件
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['file'],       # 指定file handler处理器，表示只写入到文件
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}