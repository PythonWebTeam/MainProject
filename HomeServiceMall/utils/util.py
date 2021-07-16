from account.models import Service, Type


class Util:

    @staticmethod
    def get_basic_info(request):
        # 判断用户是否已登录
        is_login = request.session.get("is_login", False)
        username = ""
        if is_login:
            username = ":" + request.session.get("username")
        # 获取全部服务种类
        services_sort = Type.objects.all()
        return username, services_sort, is_login
