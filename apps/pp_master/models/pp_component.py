from mes.sys.db import BaseModel, models
from org_com.models import Company
from .pp_warehouse import Warehouse, Location
from sys_dict.models import SysEnum
'''
部品主数据
'''
class Component(BaseModel):
    code = models.CharField(max_length=64)          # 部品代码
    name = models.CharField(max_length=128)         # 部品名称
    safe_storage = models.IntegerField(default=1)   # 安全库存数量
    facility = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='components')      # 所属工厂

    def __str__(self):
        return f'[{self.code}] - {self.name}'

    class Meta(BaseModel.Meta):
        db_table = 'pp_component'
'''
部品库存
    - 和主数据一对多关系，主要区分仓库库位对应的库存，总库存为明细和
'''
class ComponentAmount(BaseModel):
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='amounts')
    quantity = models.IntegerField(default=1)                           # 库存数量
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)  # 仓库
    location = models.ForeignKey(Location, on_delete=models.CASCADE)    # 库位

    class Meta(BaseModel.Meta):
        db_table = 'pp_component_amount'
'''
部品出入库履历
'''
class ComponentInOutList(BaseModel):
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='inouts')
    sign = models.IntegerField(default=1)       # 出入库标识 1:入 0:出 默认为入库1
    quantity = models.IntegerField(default=0)   # 出/入库数量
    inout_type = models.ForeignKey(SysEnum, on_delete=models.CASCADE)    # 出/入库类型
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)   # 出入库-仓库
    location = models.ForeignKey(Location, on_delete=models.CASCADE)     # 出入库-库位

    def __str__(self):
        return f'入库{self.quantity}' if self.sign else f'出库{self.quantity}'

    class Meta(BaseModel.Meta):
        db_table = 'pp_component_inout_list'