'''
不做Session超时检查的例外Url地址列表
'''
exclude_urls = [
    '/sys_sign/login/',
    '/sys_sign/logout/',
    '/sys_sign/relogin/',
    '/sys_sign/roles/',
    '/',
    '/test/',
    '/api/test/',
    '/api/test',
    '/api/token/get/',
    '/api/token/get',
    '/api/token/validate/',
    '/api/token/validate',
]