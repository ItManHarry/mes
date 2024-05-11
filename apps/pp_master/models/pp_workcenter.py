from mes.sys.db import models, BaseModel
from .pp_line import ProductLine
from sys_dict.models import SysEnum
from org_com.models import Company
class ProductWorkCenter(BaseModel):
    code = models.CharField(max_length=12)                                                  # 作业场代码
    name = models.CharField(max_length=128)                                                 # 作业场名称
    category = models.ForeignKey(SysEnum, on_delete=models.SET_NULL, null=True)             # 区分(对应code:D002)
    facility = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, related_name='work_centers')              # 工厂所属
    line = models.ForeignKey(ProductLine, on_delete=models.CASCADE, null=True, blank=True)  # 所属产线
    to_track = models.BooleanField(default=False)                                           # 追溯性传送
    to_sap = models.BooleanField(default=False)                                             # SAP实绩传送
    start_wc = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='start_workcenter')# Start作业场
    end_wc = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='end_workcenter')    # End作业场
    def __str__(self):
        return f'[{self.code}]{self.name}'

    class Meta(BaseModel.Meta):
        db_table = 'pp_work_center'