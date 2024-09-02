from mes.sys.db import models, BaseModel
from org_com.models import Company
class Warehouse(BaseModel):
    code = models.CharField(max_length=24)          # 仓库代码
    name = models.CharField(max_length=512)         # 仓库名称
    address = models.CharField(max_length=512)      # 仓库地点
    default = models.BooleanField(default=False)    # 默认仓库(默认否)
    facility = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='warehouses')     # 工厂代码

    def __str__(self):
        return f'[{self.code}]-{self.name}'

    class Meta(BaseModel.Meta):
        db_table = 'pp_warehouse'

class Location(BaseModel):
    code = models.CharField(max_length=24)      # 库位代码
    name = models.CharField(max_length=128)     # 库位名称
    default = models.BooleanField(default=False)  # 默认库位(默认否)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='locations')  # 所属仓库

    def __str__(self):
        return f'[{self.code}]{self.name}'

    class Meta(BaseModel.Meta):
        db_table = 'pp_location'