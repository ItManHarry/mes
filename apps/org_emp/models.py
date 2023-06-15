from mes.sys.db import models, BaseModel
from org_dep.models import Department
from django.contrib.auth.models import User
'''
组织信息-雇员信息
'''
class Employee(BaseModel):
    name = models.CharField(max_length=512)
    code = models.CharField(max_length=32)
    email = models.CharField(max_length=128, null=True)
    phone = models.CharField(max_length=24, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    photo_path = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = 'org_employee'