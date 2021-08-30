from django.http import JsonResponse
from utils.checkToken import Token    # token验证模块
from django_redis import get_redis_connection
tokenRedis = get_redis_connection('default')


def check_token(func):
    def my_function(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', 'none')
        userid = request.META.get('HTTP_USERID', 'none')
        request_path = request.META.get('PATH_INFO', 'none')
        response = {
            'code': 0,
            'msg': 'token已过期，请重新登录！',
            'datas': {}
        }
        # print(token,userid)
        # print('开启身份验证--------')
        if token == 'none' or userid == 'none':
            response['code'] = 0
            response['msg'] = '登录已过期，请重新登录！'
            response['datas']['url'] = '/'
            print('!!身份验证失败*********')
            return JsonResponse(response)
        # 生成token
        # token = Token.create_token(username, password)
        # tokenRedis.set(username, token, 86400)  # 缓存token，保存一天
        if not Token.check_token(tokenRedis, userid, token):
            response['msg'] = '身份验证失败，请重新登录！'
            print('!!身份验证失败--------')
            return JsonResponse(response)
        # print('验证通过！！！！')
        return func(request, *args, **kwargs)
    return my_function
