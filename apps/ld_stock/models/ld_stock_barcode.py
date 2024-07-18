from mes.sys.db import models, BaseModel
from pp_master.models.pp_component import Component
from org_com.models import Company
class StockBarCode(BaseModel):
    '''
    使用active栏位控制是否全部入库完毕即可
    1：入库未完成 0：入库完成
    逻辑：
    barcode明细全部入库完毕方可设置为入库完毕
    '''
    code = models.CharField(max_length=32)
    facility = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.code
    class Meta(BaseModel.Meta):
        db_table = 'ld_stock_barcode'

class StockBarCodeList(BaseModel):
    barcode = models.ForeignKey(StockBarCode, on_delete=models.CASCADE, related_name='items')
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    '''
    数量和入库数量相等是，active设置为False，即当前明细对应的部品入库完毕
    '''
    amount = models.IntegerField(default=1)         # 数量
    amount_in = models.IntegerField(default=0)      # 已入库数量

    class Meta(BaseModel.Meta):
        db_table = 'ld_stock_barcode_list'

