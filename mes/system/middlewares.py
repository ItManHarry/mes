# middlewares
def session_check(get_response):
    def check(request):
        print('Do the session check before the the view are called .........')
        response = get_response(request)
        print('Do the session check after the view are called ............')
        return response
    return check