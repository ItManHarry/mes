urlpatterns = []
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore, register_job
# # 实例化调度器
# scheduler = BackgroundScheduler()
# # 开启定时工作
# # 调度器使用DjangoJobStore()
# scheduler.add_jobstore(DjangoJobStore(), "default")
# # 设置定时任务，选择方式为interval，时间间隔为10s
# # 另一种方式为每天固定时间执行任务，对应代码为：
# # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
# @register_job(scheduler, "interval", seconds=10, id='test_job', replace_existing=True)  # replace_existing=解决第二次启动失败的问题
# def my_job():
#     # 这里写你要执行的任务
#     print('This is my apscheduler job ...')
# scheduler.start()