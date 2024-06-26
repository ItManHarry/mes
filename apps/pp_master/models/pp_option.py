from mes.sys.db import models, BaseModel
from org_com.models import Company
from .pp_machinecode import ModelCode
class OptionBasic(BaseModel):
    code = models.CharField(max_length=24)          # Option代码
    name = models.CharField(max_length=24)          # Option名称
    sequence = models.CharField(max_length=24)      # 顺序
    use = models.BooleanField(default=True)         # 在用
    facility = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='options')     # 工厂

    def __str__(self):
        return f'[{self.code}]{self.name}'

    class Meta(BaseModel.Meta):
        db_table = 'pp_option_basic'
class OptionCode(BaseModel):
    code = models.CharField(max_length=48)                                      # Option代码
    style_code = models.CharField(max_length=16)                                # 式样代码
    o_sap = models.CharField(max_length=256)                                    # Option说明(SAP)
    s_sap = models.CharField(max_length=256)                                    # 式样说明(SAP)
    o_mes = models.CharField(max_length=256)                                    # Option说明(MES)
    s_mes = models.CharField(max_length=256)                                    # 式样说明(MES)
    basic = models.BooleanField(default=False)                                  # 基本Option
    erp_if = models.BooleanField(default=True)                                  # ERP接口
    sign = models.BooleanField(default=False)                                   # 详细标识
    option = models.ForeignKey(OptionBasic, on_delete=models.CASCADE)           # Option信息所属
    model_styles = models.ManyToManyField(ModelCode, related_name='options')    # 代表式样所属
    facility = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='option_codes')    # 工厂
    def __str__(self):
        return self.code

    class Meta(BaseModel.Meta):
        db_table = 'pp_option_code'