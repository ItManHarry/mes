from mes.sys.db import models, BaseModel
from org_com.models import Company
from sys_dict.models import SysEnum
from . import ProductLine
'''
机种信息表
'''
class MachineCode(BaseModel):
    code = models.CharField(max_length=8)       # 机种代码
    model_sap = models.CharField(max_length=128, null=True, blank=True)     # SAP机型代码
    model_mes = models.CharField(max_length=128, null=True, blank=True)     # MES机型代码
    pro_group1 = models.CharField(max_length=128, null=True, blank=True)    # 产品Group1
    pro_group2 = models.CharField(max_length=128, null=True, blank=True)    # 产品Group2
    pro_quality = models.ForeignKey(SysEnum, on_delete=models.CASCADE)      # 品质产品群(代码：D003)
    lines = models.ManyToManyField(ProductLine)     # 对应产线
    finished = models.BooleanField(default=False)   # 是否结束(即是否还生产)
    facility = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='machine_codes')  # 工厂

    def __str__(self):
        return f'[{self.code}]-{self.model_mes}'


    class Meta(BaseModel.Meta):
        db_table = 'pp_machine_code'
'''
机型代表式样信息表
'''
class ModelCode(BaseModel):
    code = models.CharField(max_length=128)                                 # 代表式样代码
    brand_code = models.CharField(max_length=64, null=True, blank=True)     # 铭牌机种名
    weight_sap = models.IntegerField(default=0)                             # 机种重量(SAP)
    weight_brand = models.IntegerField(default=0)                           # 机种重量(铭牌)
    engine_no = models.CharField(max_length=128, null=True, blank=True)     # 发动机品号
    remark = models.TextField(null=True, blank=True)                        # 备注
    cup = models.ForeignKey(SysEnum, on_delete=models.CASCADE, related_name='cups', null=True)             # CUP(代码：D004)
    machine_type = models.ForeignKey(SysEnum, on_delete=models.CASCADE, related_name='mts', null=True)     # 设备类型(代码：D005)
    sale_type = models.ForeignKey(SysEnum, on_delete=models.CASCADE, related_name='sts', null=True)        # 销售类型(代码：D006)
    product = models.BooleanField(default=False)                                # 是否断种(即是否还生产)
    machine_code = models.ForeignKey(MachineCode, on_delete=models.CASCADE)     # 机种所属
    facility = models.ForeignKey(Company, on_delete=models.CASCADE)             # 工厂

    def __str__(self):
        return self.model_mes


    class Meta(BaseModel.Meta):
        db_table = 'pp_model_code'