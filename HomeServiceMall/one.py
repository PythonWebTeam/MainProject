from operator import itemgetter
import pymysql
import math

'''
HOST = '119.45.125.97'
USER = 'root'
PASSWORD = '123456'
DATABASE = 'django_mysql'
PORT = 3306

#连接数据库
def get_db():
    return pymysql.connect(HOST,USER,PASSWORD,DATABASE,PORT)

# 执行查询多条的sql语句
def select(sql):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except:
        db.rollback()
    finally:
        db.close()


# 执行查询单条的sql语句
def select_one(sql):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        return result
    except:
        db.rollback()
    finally:
        db.close()

# 读出所要的数据
def get_data():
    sql = 'SELECT userorder.user_id, userorder.service_id,service.img1, service.title FROM Order userorder, Service service WHERE service.id = userorder.service_id'
    result = select(sql)

    print("查询结果为：")
    for row in result:
        print(row)
    data = {}
    for row in result:
        if row[0] not in data:
            data[row[0]] = []
        data[row[0]].append({'id': row[1], 'img': row[2], 'title': row[3])
    print('查询结果为：')
    for key,value in data.items():
        print(key,":",value)

    return result
'''

'''
result
user_id   service_id   img1  title   
1
2
'''



# 根据用户购买商品的余弦相似度推荐算法
def recommend(user_id, user_num, recommend_num):
    result = ((1, 1, '商品1图片路径', '商品1', 300), (1, 2, '商品2图片路径', '商品2', 150),
              (2, 2, '商品2图片路径', '商品2', 150),(2, 3, '商品3图片路径', '商品3', 400),
              (3, 1, '商品1图片路径', '商品1', 300),
              (4, 3, '商品3图片路径', '商品3', 400),
              (5, 1, '商品1图片路径', '商品1', 300),(5, 2, '商品2图片路径', '商品2', 150),(5, 4, '商品4图片路径', '商品4', 450),
              (6, 1, '商品1图片路径', '商品1', 300),(6, 3, '商品3图片路径', '商品3', 400),
              (7, 1, '商品1图片路径', '商品1', 300),(7, 4, '商品4图片路径', '商品4', 450),(7, 5, '商品2图片路径', '商品2', 350),
              (8, 1, '商品1图片路径', '商品1', 300),(9, 2, '商品2图片路径', '商品2', 150))

    '''
    print('查询结果为:')
    for row in result:
        print(row)
    '''

    #result = get_data()
    user_goods_info = {}  # 带有详细信息的数据矩阵{用户：【商品及其信息。。。】。。。}
    user_goods_matrix = {}  # 用户商品矩阵只有用户编号和商品编号的数据矩阵，便于算法使用{用户：【商品。。。】。。。}
    for row in result:
        if row[0] not in user_goods_matrix:
            user_goods_info.setdefault(row[0], [])
            user_goods_matrix.setdefault(row[0], [])
        user_goods_info[row[0]].append({'id': row[1], 'img': row[2], 'title': row[3]})
        user_goods_matrix[row[0]].append(row[1])

    '''
    user_goods_info
    user_id   id   img   title   sales
    {1: [{'id': 1, 'img': '商品1图片路径', 'title': '商品1', 'sales': 300}, 
         {'id': 2, 'img': '商品2图片路径', 'title': '商品2', 'sales': 150}], 
     2: [{'id': 2, 'img': '商品2图片路径', 'title': '商品2', 'sales': 150}, 
         {'id': 3, 'img': '商品3图片路径', 'title': '商品3', 'sales': 400}], 
     3: [{'id': 1, 'img': '商品1图片路径', 'title': '商品1', 'sales': 300}], 
     4: [{'id': 3, 'img': '商品3图片路径', 'title': '商品3', 'sales': 400}], 
     5: [{'id': 1, 'img': '商品1图片路径', 'title': '商品1', 'sales': 300}], 
     6: [{'id': 2, 'img': '商品2图片路径', 'title': '商品2', 'sales': 150}], 
     7: [{'id': 1, 'img': '商品1图片路径', 'title': '商品1', 'sales': 300}], 
     8: [{'id': 1, 'img': '商品1图片路径', 'title': '商品1', 'sales': 300}], 
     9: [{'id': 2, 'img': '商品2图片路径', 'title': '商品2', 'sales': 150}]}
    user_goods_matrix
    user_id id
    {1: [1, 2], 2: [2, 3], 3: [1], 4: [3], 5: [1], 6: [2], 7: [1], 8: [1], 9: [2]}
    '''

    good_user_matrix = {}  # 商品用户矩阵，将用户商品矩阵 user_goods_matrix 转换为商品用户矩阵 good_user_matrix，{商品：【用户。。。】。。。}
    for user, goods in user_goods_matrix.items():
        for good in goods:
            if good not in good_user_matrix:
                good_user_matrix.setdefault(good, set())
            good_user_matrix[good].add(user)

    '''
   
        
    good_user_matrix
    {1: {1, 3, 5, 7, 8}, 2: {1, 2, 6, 9}, 3: {2, 4}}
    '''

    user_inner_matrix = {}  # 用户之间相同商品数量矩阵，统计用户之间购买过相同商品的数量{用户1：{用户2：相同商品数，。。。}。。。}
    for users in good_user_matrix.values():    #users: {{1,3},{2},{4}}
        for user1 in users:
            for user2 in users:
                if user1 == user2:
                    continue
                if user1 not in user_inner_matrix:
                    user_inner_matrix.setdefault(user1, {})
                if user2 not in user_inner_matrix[user1]:
                    user_inner_matrix[user1][user2] = 0
                user_inner_matrix[user1][user2] += 1

    '''
    user_inner_matrix
   {1: {3: 1, 5: 1, 7: 1, 8: 1, 2: 1, 6: 1, 9: 1}, 
    3: {1: 1, 5: 1, 7: 1, 8: 1}, 
    5: {1: 1, 3: 1, 7: 1, 8: 1}, 
    7: {1: 1, 3: 1, 5: 1, 8: 1}, 
    8: {1: 1, 3: 1, 5: 1, 7: 1}, 
    2: {1: 1, 6: 1, 9: 1, 4: 1}, 
    6: {1: 1, 2: 1, 9: 1}, 
    9: {1: 1, 2: 1, 6: 1}, 
    4: {2: 1}}
    '''
    user_similar_matrix = {}  # 用户之间相似度矩阵，计算用户之间的相似度{用户1：{用户2：相似度，。。。}。。。}
    for user1, inner in user_inner_matrix.items():
        for user2, num in inner.items():
            if user1 not in user_similar_matrix:
                user_similar_matrix.setdefault(user1, {})
            if user2 not in user_similar_matrix[user1]:
                user_similar_matrix[user1][user2] = 0
            user_similar_matrix[user1][user2] = num / math.sqrt(len(user_goods_matrix[user1]) * len(user_goods_matrix[user2]))   #余弦相似度

    '''
    user_similar_matrix
   {1: {3: 0.7071067811865475, 5: 0.7071067811865475, 7: 0.7071067811865475, 8: 0.7071067811865475, 2: 0.5, 6: 0.7071067811865475, 9: 0.7071067811865475}, 
    3: {1: 0.7071067811865475, 5: 1.0, 7: 1.0, 8: 1.0}, 
    5: {1: 0.7071067811865475, 3: 1.0, 7: 1.0, 8: 1.0}, 
    7: {1: 0.7071067811865475, 3: 1.0, 5: 1.0, 8: 1.0}, 
    8: {1: 0.7071067811865475, 3: 1.0, 5: 1.0, 7: 1.0}, 
    2: {1: 0.5, 6: 0.7071067811865475, 9: 0.7071067811865475, 4: 0.7071067811865475}, 
    6: {1: 0.7071067811865475, 2: 0.7071067811865475, 9: 1.0}, 
    9: {1: 0.7071067811865475, 2: 0.7071067811865475, 6: 1.0}, 
    4: {2: 0.7071067811865475}}
    '''
    user_goods = user_goods_matrix[user_id]  # 目标用户的商品集合
    """
                       key=itemgetter(1)           按值排序
                       reverse=True                降序排列
    """
    user_similar_matrix = sorted(user_similar_matrix[user_id].items(), key=itemgetter(1), reverse=True)[:user_num]  # 和目标用户的相似用户相似度排序

    print('目标用户的商品集合', user_goods)

    '''
    user_goods
    [1,2]
    
    排序删选后user_similar_matrix
    [(5, 0.8164965809277261), (6, 0.8164965809277261), (3, 0.7071067811865475), (7, 0.7071067811865475), (8, 0.7071067811865475)]
    '''

    good_ids = {}  # 要推荐的商品的序号及相似度（未排序）
    for user, similar in user_similar_matrix:
        print(user, ':', similar)
        for goods in user_goods_matrix[user]:
            if goods in user_goods:
                continue
            if goods not in good_ids:
                good_ids.setdefault(goods, 0)
            good_ids[goods] += similar

    print('排序前的商品的序号及相似度', good_ids)
    good_ids = sorted(good_ids.items(), key=itemgetter(1), reverse=True)[:recommend_num]  # 排序后的商品的序号及相似度
    print('排序后的商品的序号及相似度', good_ids)
    count_sort = []  # 要推荐的商品的序号
    for id in good_ids:
        count_sort.append(id[0])
    print('推荐的商品的序号', count_sort)

    goods_data = []  # 所有商品信息数组
    for user in user_goods_info.keys():
        for good in user_goods_info[user]:   #一个good包括'id':1,'img'='地址','title' = 'a'
            if good not in goods_data:
                goods_data.append(good)

    recommend_goods = []  # 要推荐的详细商品
    for id in count_sort:
        for good in goods_data:
            if id == good['id'] and good not in recommend_goods:
                recommend_goods.append(good)



    return recommend_goods


if __name__ == '__main__':
    for good in recommend(1,5,2):                  #推荐4个
        print(good)

