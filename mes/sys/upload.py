import os
import time
from django.conf import settings
def handle_uploaded_file(file=None, upload_path=None):
    if file:
        now_stamp = time.time()
        print('Time stamp is : ', int(now_stamp))
        file_extend = '.' + file.name.split('.')[1]     # 获取文件扩展名
        file_name = str(int(now_stamp)) + file_extend   # 重命名文件(时间戳为文件名)
        print('New file name is : ', file_name)
        file_path = upload_path+'/'+file_name           # 文件文件保存到数据库
        upload_path = os.path.join(settings.UPLOAD_FILE_PATH, upload_path)
        # 文件上传路径-文件夹若不存在，执行创建
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        file_to_upload = os.path.join(upload_path, file_name)
        # 执行上传
        with open(file_to_upload, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return file_path
    return None