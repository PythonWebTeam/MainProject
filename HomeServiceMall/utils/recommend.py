from operator import itemgetter
import pymysql

from account.models import Order, Service

'''
购买过1的用户还购买过

{1: [ {'id': 2, 'img': '商品2图片路径', 'title': '商品2'}], 
2: [{'id': 4, 'img': '商品4图片路径', 'title': '商品4'},{'id': 3, 'img': '商品3图片路径', 'title': '商品3'}], 
4: [{'id': 3, 'img': '商品3图片路径', 'title': '商品3'}], 
5: [{'id': 4, 'img': '商品4图片路径', 'title': '商品4'},{'id': 5, 'img': '商品5图片路径', 'title': '商品5'}], 
7: [{'id': 2, 'img': '商品2图片路径', 'title': '商品2'}],
8: [{'id': 2, 'img': '商品2图片路径', 'title': '商品2'},{'id': 6, 'img': '商品6图片路径', 'title': '商品6'}]}
'''


# 购买过此商品的用户还购买过推荐算法
def recommend(service, count):  # 用户购买过serviceId服务,推荐数量为count的相似服务
    orders_all = Order.objects.filter(service=service)
    service_count = {}
    for order_all in orders_all:
        orders_person = order_all.user.get_all_orders()
        for order_person in orders_person:
            if order_person.service.id == service.id:
                continue
            else:
                if order_person.service.id not in service_count:
                    service_count[order_person.service.id] = 1
                service_count[order_person.service.id] += 1
    '''
    service_count
    {2: 3, 4: 2, 3: 2, 5: 1, 6: 1}
    '''
    if count < len(service_count):
        services_count_sort = sorted(service_count.items(), key=itemgetter(1), reverse=True)[:count]
    else:
        services_count_sort = sorted(service_count.items(), key=itemgetter(1), reverse=True)
    count_sort = []
    for service_id in services_count_sort:
        count_sort.append(service_id[0])
    recommend_services = []
    for id in count_sort:
        service_add = Service.objects.get(id = id)
        if service not in recommend_services:
            recommend_services.append(service_add)
    return recommend_services


'''
[{'id': 2, 'img': '商品2图片路径', 'title': '商品2'}, {'id': 4, 'img': '商品4图片路径', 'title': '商品4'}, {'id': 3, 'img': '商品3图片路径', 'title': '商品3'}]
'''
if __name__ == '__main__':
    # get_data(1)
    for service in recommend(1, 3):
        print(service)
