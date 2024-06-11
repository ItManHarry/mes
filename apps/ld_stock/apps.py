from django.apps import AppConfig

'''
物流库存模块
主要进行配件的出入库管理
'''
class LdStockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ld_stock'
