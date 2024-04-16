from mes.sys.db import models, BaseModel
from org_com.models import Company
'''
组织信息-部门信息
'''
class Department(BaseModel):
    name = models.CharField(max_length=512)
    code = models.CharField(max_length=32)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_pp_rel_dept = models.BooleanField(default=False)         # 生产关联部门
    is_pp_dept = models.BooleanField(default=False)             # 生产部门
    is_hv_dept = models.BooleanField(default=False)             # Heavy 部门
    is_qc_dept = models.BooleanField(default=False)             # 品质部门
    is_an_handle_dept = models.BooleanField(default=False)      # 异常申告处理部门
    is_wk_handle_dept = models.BooleanField(default=False)      # 作业邀请处理部门


    @property
    def children(self):
        return Department.objects.filter(parent_id=self.id)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = 'org_department'