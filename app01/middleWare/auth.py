# 自定义django中间件

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class M1(MiddlewareMixin):
    """ 中间件1 """

    def process_request(self, request):
        # 1.排除那些不需要登录就能访问的页面
        # request.path_info获取当前用户请求的URL
        if request.path_info in ['/login/','/image/code/' ]:
            return None
        # 2.登录验证，若存在session，说明登录过，继续往下一个中间件走
        info_dict = request.session.get('info')
        if info_dict:
            return None
        # 3.若没有登录，重定向
        return redirect('/login/')

    def process_response(self, request, response):

        return response