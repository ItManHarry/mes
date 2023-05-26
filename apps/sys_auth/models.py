from mes.sys.db import BaseModel, models
from django.contrib.auth.models import User
from org_com.models import Company
'''
系统菜单
'''
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
'''
系统角色
'''
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

'''
最近使用菜单
'''
class RecentUsedMenu(BaseModel):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)             # 使用菜单
    user = models.ForeignKey(User, on_delete=models.CASCADE)             # 用户
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)  # 对应角色（当为超级管理员是，此栏位为空）

    class Meta(BaseModel.Meta):
        db_table = 'sys_rencent_used_menu'