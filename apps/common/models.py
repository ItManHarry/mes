from mes.sys.db import models, BaseModel
from django.contrib.auth.models import User

class SysLog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)        # 操作用户ID
    url = models.CharField(max_length=32, null=True)                # 操作菜单URL
    ip = models.CharField(max_length=32, null=True)                 # 操作用户IP地址

    def __str__(self):
        return 'User is {}, operate module url {}.'.format(self.user.username, self.url)

    class Meta(BaseModel.Meta):
        db_table = 'sys_log'