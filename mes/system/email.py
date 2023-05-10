from django.core.mail import EmailMultiAlternatives
from django.template import loader
from threading import Thread
def exe_send_mail(email):
    email.send()
def send_mail(subject, to, template, context={}, cc=[], body=None, attachment=None):
    '''
    启动邮件发送线程，异步发送邮件
    :param subject:     邮件标题
    :param to:          收件人清单(List类型)
    :param template:    html模板文件
    :param context:     html模板数据
    :param cc:          参照人
    :param body:        邮件文本内容
    :param attachment:  附件
    :return:
    '''
    email = EmailMultiAlternatives(subject=subject, to=to)
    t = loader.get_template(template)
    html_content = t.render(context)
    email.attach_alternative(html_content, 'text/html')
    if cc:
        email.cc = cc
    if body:
        email.body = body
    if attachment:
        email.attach_file(attachment)
    thread = Thread(target=exe_send_mail, args=[email])
    thread.start()
    return thread