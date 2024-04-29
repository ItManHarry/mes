from mes.sys.db import models, BaseModel
from org_com.models import Company
from sys_dict.models import SysEnum
from . import ProductLine
'''
机种信息表
'''
class MachineCode(BaseModel):
    code = models.CharField(max_length=8)       # 机种代码
    pro_group1 = models.CharField(max_length=128, null=True, blank=True)            # 产品Group1
    pro_group2 = models.CharField(max_length=128, null=True, blank=True)            # 产品Group2
    pro_quality = models.ForeignKey(SysEnum, on_delete=models.CASCADE)  # 品质产品群(代码：D003)
    lines = models.ManyToManyField(ProductLine)     # 对应产线
    finished = models.BooleanField(default=False)   # 是否结束(即是否还生产)
    facility = models.ForeignKey(Company, on_delete=models.CASCADE)  # 工厂

    def __str__(self):
        return f'[{self.code}]{self.name}'


    class Meta(BaseModel.Meta):
        db_table = 'pp_machinecode'
'''
机型信息表
'''
class ModelCode(BaseModel):
    model_sap = models.CharField(max_length=128)  # SAP机型代码
    model_mes = models.CharField(max_length=128)  # MES机型代码
    machine_code = models.ForeignKey(MachineCode, on_delete=models.CASCADE)     # 机种所属
    facility = models.ForeignKey(Company, on_delete=models.CASCADE)             # 工厂

    def __str__(self):
        return self.model_mes


    class Meta(BaseModel.Meta):
        db_table = 'pp_modelcode'