from django.utils.deprecation import MiddlewareMixin


class Middleweare(MiddlewareMixin):
    print('初始化')
    def process_request(self,request):
        pass
    def process_response(self,request,response):
        response['X-Frame-Option'] = 'SAMEORING'
        return response


