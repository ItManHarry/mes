from mes.sys.db import models, BaseModel
from pp_master.models import Component
from pp_master.models import Warehouse, Location
from .ld_stock import StockBill
'''
出入库单明细
'''
class StockItems(BaseModel):
    bill = models.ForeignKey(StockBill, on_delete=models.CASCADE)       # 出入库单
    component = models.ForeignKey(Component, on_delete=models.CASCADE)  # 配件
    amount = models.IntegerField(default=1)                             # 数量
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)  # 仓库
    location = models.ForeignKey(Location, on_delete=models.CASCADE)    # 库位
    tmp_bill_id = models.CharField(max_length=32, null=True)            # 临时单据ID

    class Meta(BaseModel.Meta):
        db_table = 'ld_stock_items'