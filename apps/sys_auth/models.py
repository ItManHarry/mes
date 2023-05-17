from mes.sys.db import BaseModel, models
from django.contrib.auth.models import User
from org_com.models import Company

class Menu(BaseModel):
    name = models.CharField(max_length=64)      # 菜单名称
    code = models.CharField(max_length=24)      # 菜单代码
    url = models.CharField(max_length=24)       # 链接地址
    icon = models.CharField(max_length=24)      # 菜单图标
    remark = models.CharField(max_length=256, blank=True, null=True)   # 菜单描述

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = 'sys_menu'

class Role(BaseModel):
    name = models.CharField(max_length=64)  # 角色名称
    code = models.CharField(max_length=24)  # 角色代码
    users = models.ManyToManyField(User)    # 角色用户
    menus = models.ManyToManyField(Menu)    # 角色菜单
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = 'sys_role'