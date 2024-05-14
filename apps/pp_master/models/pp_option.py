from mes.sys.db import models, BaseModel
from org_com.models import Company
class OptionBasic(BaseModel):
    code = models.CharField(max_length=24)          # Option代码
    style_code = models.CharField(max_length=16)    # 式样代码
    o_remark = models.CharField(max_length=256)     # Option说明
    s_remark = models.CharField(max_length=256)     # 式样说明
    facility = models.ForeignKey(Company, on_delete=models.CASCADE)     # 工厂

    def __str__(self):
        return f'{self.code}_{self.style_code}'

    class Meta(BaseModel.Meta):
        db_table = 'pp_option_basic'