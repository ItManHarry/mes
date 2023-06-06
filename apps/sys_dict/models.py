from django.db import models
from mes.sys.db import BaseModel

class SysDict(BaseModel):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = 'sys_dict'

class SysEnum(BaseModel):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=4)
    sys_dict = models.ForeignKey(SysDict, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = 'sys_enum'