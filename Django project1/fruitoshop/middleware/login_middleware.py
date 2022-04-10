from django.shortcuts import redirect, render
from django.utils.deprecation import MiddlewareMixin

loginRequired_list = ['/detail/', '/receive_address/', '/order/', '/logout/', '/show_my_cart/']


# 以下可自定义中间件函数
class LoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path in loginRequired_list:
            # 自己存session使用
            # username = request.session.get('username')
            # if not username:
            #     return redirect('/user_login/')

            # 使用内置登录方法自动存session使用is_authenticated验证是否登录，模板中也可以使用
            if not request.user.is_authenticated:
                return redirect('/user_login/')

    # def process_view(self, request, callback, callback_args, callback_kwargs):
    #     pass
    #
    # def process_response(self, request, response):
    #     return response
    #
    # def process_template_response(self):
    #     pass

    # def process_exception(self, request, exception):
    #     print(exception)
    #     return render(request, '500.html')
