from mes.sys.db import models, BaseModel
from org_com.models import Company

class ProductLine(BaseModel):
    name = models.CharField(max_length=24)      # 产线名称
    code = models.CharField(max_length=8)       # 产线代码
    version = models.CharField(max_length=4)    # 版本
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='product_lines')  # 工厂所属

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = 'pp_product_line'