from django.db import models
import time, datetime
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
class BaseModel(models.Model):
    class Meta:
        abstract = True
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)                     # ID
    active = models.BooleanField(default=True)                                      # 是否可用(默认可用)
    created_by = models.IntegerField(null=True)                                     # 创建人
    created_on = models.DateTimeField(default=timezone.now, editable=False)         # 创建时间(UTC时间)
    updated_by = models.IntegerField(null=True)                                     # 更新人
    updated_on = models.DateTimeField(default=timezone.now)                         # 更新时间(UTC时间)

    @property
    def created(self):
        if self.created_by:
            return User.objects.get(pk=self.created_by)
        return None

    @property
    def updated(self):
        if self.updated_by:
            return User.objects.get(pk=self.updated_by)
        return None

    def get_created_on(self, off_set=None):
        return self.utc_to_locale(self.created_on, off_set)

    def get_updated_on(self, off_set=None):
        return self.utc_to_locale(self.updated_on, off_set)


    def utc_to_locale(self, utc_date_time, off_set=None):
        '''
        UTC时间转本地
        :param utc_date_time:   UTC时间
        :param off_set:         时区(如果为None则默认转为本地时区)
        :return:
        '''
        now_stamp = time.time()
        locale_time = datetime.datetime.fromtimestamp(now_stamp)
        utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
        # 计算时差
        if off_set is None:
            off_set = locale_time - utc_time
        else:
            off_set = datetime.timedelta(hours=off_set)
        locale_date_time = utc_date_time + off_set
        return locale_date_time