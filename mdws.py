# middlewares
def test_middleware(get_response):
    def middleware(request):
        print('Do the middleware action before the the view are called .........')
        response = get_response(request)
        print('Do the middleware action after the view are called ............')
        return response
    return middleware