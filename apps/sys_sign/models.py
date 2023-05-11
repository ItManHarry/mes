from django.db import models
from django.contrib.auth.models import User
from mes.sys.db import BaseModel
class SysLogin(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # 登录用户ID
    ip = models.CharField(max_length=32, null=True)             # 登录IP地址

    def __str__(self):
        return 'Login user is {}, login ip address {}.'.format(self.user.username, self.ip)

    class Meta(BaseModel.Meta):
        db_table = 'sys_login'