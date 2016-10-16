"""dang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01.views import submit, exam, acc_login, up_users,updata,acc_logout, cul_mask, index_aa, survey, surveydata,download_mask, upload_file,upload




urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index_aa),       # 进入首页
    url(r'accounts/login/', acc_login, name='login'),   # 登录页面
    url(r'logout/', acc_logout, name='logout'),  # 退出登录
    url(r'updata/$', updata),       # 上传数据到数据库
    url(r'exam/$', exam),       # 进入考试
    url(r'submit/$', submit),   # 提交试卷
    url(r'survey/$', survey, name='survey'),     # 调查问卷
    url(r'surveydata/$', surveydata, name='surveydata'),    # 提交问卷数据
    url(r'mask/$', cul_mask, name='culmask'),  # 计算成绩
    url(r'download/$', download_mask, name='download'),     # 下载成绩单
    url(r'upload/$', upload),       # 上传页面
    url(r'uploadfile/$', upload_file),  # 上传xls到指定目录
]
