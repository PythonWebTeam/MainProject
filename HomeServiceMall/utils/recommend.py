from operator import itemgetter
from account.models import Order, Service


# 购买过此商品的用户还购买过推荐算法

def recommend(service, count):  # 用户购买过serviceId服务,推荐数量为count的相似服务
    orders_all = Order.objects.filter(service=service)
    service_count = {}
    for order_all in orders_all:                             # 统计购买过此商品用户的所有用户的订单频率
        orders_person = order_all.user.get_all_orders()
        for order_person in orders_person:
            if order_person.service.id == service.id:
                continue
            else:
                if order_person.service.id not in service_count:
                    service_count[order_person.service.id] = 1
                service_count[order_person.service.id] += 1
    if count < len(service_count):            # 如果能推荐的商品少于目标数，则排序后直接推荐
        services_count_sort = sorted(service_count.items(), key=itemgetter(1), reverse=True)[:count]
    else:                                     # 如果能推荐的商品大于目标数，则排序后切片后直接推荐
        services_count_sort = sorted(service_count.items(), key=itemgetter(1), reverse=True)
    count_sort = []
    for service_id in services_count_sort:
        count_sort.append(service_id[0])
    recommend_services = []                        # 统计推荐的service_id
    for id in count_sort:
        service_add = Service.objects.get(id=id)
        if service not in recommend_services:
            recommend_services.append(service_add)   # 返回推荐服务
    return recommend_services
