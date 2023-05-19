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

    @property
    def children(self):
        return Department.objects.filter(parent_id=self.id)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = 'org_department'