from mes.sys.db import models, BaseModel
from sys_dict.models import SysEnum
from django.utils import timezone
from django.contrib.auth.models import User
from org_com.models import Company

class StockBill(BaseModel):
    bill_no = models.CharField(max_length=32, blank=True)               # 单号(自动创建)
    bill_type = models.ForeignKey(SysEnum, on_delete=models.CASCADE, related_name='type_bills')     # 单据类型(对应code: D009 出库/入库)
    bill_date = models.DateField(timezone.now)                          # 日期-默认当天
    in_out_type = models.ForeignKey(SysEnum, on_delete=models.CASCADE, related_name='in_out_bills')  # 出入库对应code: D007/DOO8
    in_out_by = models.ForeignKey(User, on_delete=models.CASCADE)       # 出入库人员
    facility = models.ForeignKey(Company, on_delete=models.CASCADE)     # 工厂所属

    def __str__(self):
        return self.bill_no

    class Meta(BaseModel.Meta):
        db_table = 'ld_stock_bill'
