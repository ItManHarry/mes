from mes.sys.db import models, BaseModel
'''
组织信息-公司信息
'''
class Company(BaseModel):
    name = models.CharField(max_length=512)     # 公司名称
    code = models.CharField(max_length=32)      # 公司代码

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = 'org_company'