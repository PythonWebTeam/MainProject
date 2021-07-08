from django.db import models

# Create your models here.
"""
创建学生信息表模型
"""
from django.db import models

"""
 该类是用来生成数据库的 必须要继承models.Model
"""
class Student(models.Model):
    """
    创建如下几个表的字段
    """
    # 学号 primary_key=True: 该字段为主键
    studentNum = models.CharField('学号', primary_key=True, max_length=15)
    # 姓名 字符串 最大长度20
    name = models.CharField('姓名', max_length=20)
    # 年龄 整数 null=False, 表示该字段不能为空
    age = models.IntegerField('年龄', null=False)
    # 性别 布尔类型 默认True: 男生 False:女生
    sex = models.BooleanField('性别', default=True)
    # 手机 unique=True 该字段唯一
    mobile = models.CharField('手机', unique=True, max_length=15)
    # 创建时间 auto_now_add：只有在新增的时候才会生效
    createTime = models.DateTimeField(auto_now_add=True)
    # 修改时间 auto_now： 添加和修改都会改变时间
    modifyTime = models.DateTimeField(auto_now=True)

    # 指定表名 不指定默认APP名字——类名(app_demo_Student)
    class Meta:
        db_table = 'student'


"""
学生社团信息表
"""
class studentUnion(models.Model):
    # 自增主键, 这里不能设置default属性，负责执行save的时候就不会新增而是修改元素
    id = models.IntegerField(primary_key=True)
    # 社团名称
    unionName = models.CharField('社团名称', max_length=20)
    # 社团人数
    unionNum = models.IntegerField('人数', default=0)
    # 社团负责人 关联Student的主键 即studentNum学号 一对一的关系,on__delete 属性在django2.0之后为必填属性后面会介绍
    # unionRoot = models.OneToOneField(Student, on_delete=None)

    class Meta:
        db_table = 'student_union'


"""
OneToOneField： 一对一
ForeignKey: 一对多
ManyToManyField： 多对多(没有ondelete 属性)
"""