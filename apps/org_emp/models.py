from mes.sys.db import models, BaseModel
from org_dep.models import Department
from django.contrib.auth.models import User
from pp_master.models.pp_workcenter import ProductWorkCenter
'''
组织信息-雇员信息
'''
class Employee(BaseModel):
    name = models.CharField(max_length=512)
    code = models.CharField(max_length=32)
    email = models.CharField(max_length=128, null=True)
    phone = models.CharField(max_length=24, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='employee')
    photo_path = models.CharField(max_length=128, null=True)
    work_center = models.ForeignKey(ProductWorkCenter, on_delete=models.SET_NULL,
                                    null=True, related_name='employees')    # 当前作业场所属
    def __str__(self):
        return self.name
    class Meta(BaseModel.Meta):
        db_table = 'org_employee'
'''
雇员作业场变更履历
'''
class EmployeeWorkCenterChangeList(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='work_center_list')
    department = models.CharField(max_length=512, null=True)
    work_center = models.ForeignKey(ProductWorkCenter, on_delete=models.CASCADE, related_name='employee_list')
    class Meta(BaseModel.Meta):
        db_table = 'employee_work_center_change_list'