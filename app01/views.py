from django.shortcuts import render,HttpResponse,redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from app01 import models
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django import forms

class Log_in(forms.Form):
    user=forms.CharField(
                         error_messages={'required': '用户不能为空'},
                         widget=forms.TextInput(attrs={'class':"form-control",'placeholder':'用户名'})
                         )
    pwd=forms.CharField(min_length=3,
                        error_messages={'required': '密码不能为空'},
                        widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':'密码'}))

class Regist(forms.Form):
    username=forms.CharField(
                         error_messages={'required': '用户名错误'},
                         widget=forms.TextInput(attrs={'class':"form-control",'placeholder':'用户名'})
                         )
    password=forms.CharField(min_length=3,
                        error_messages={'required': '密码错误'},
                        widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':'密码'}))



def log_in(request):
    if request.method=='GET':
        obj=Log_in()
        return render(request, 'login.html',locals())
    else:
        obj=Log_in(request.POST)
        if obj.is_valid():
            data=obj.cleaned_data
            user = auth.authenticate(username=data.get('user'),password=data.get('pwd'))
            if user:
                auth.login(request,user)
                return redirect('/index/')
            else:
                return render(request, 'login.html', {'obj': obj})
        else:
            return render(request, 'login.html',{'obj':obj})




def register(request):
    if request.method=='GET':
        obj=Regist()
        return render(request, 'register.html',{'obj':obj})
    else:
        obj=Regist(request.POST)
        if obj.is_valid():
            data=obj.cleaned_data
            User.objects.create_user(**data)
        return redirect('/login/')

def set_password(request):
    if request.method=='GET':
        return render(request,'set_password.html')
    else:
        oldpwd=request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        user=request.user
        if user.check_password(oldpwd):
            user.set_password(newpwd)
            user.save()
            return redirect('/login/')

def logout(request):
    auth.logout(request)
    return redirect('/login/')


@login_required
def index(request):
    page_number = request.GET.get("page")
    book_lists = models.Book.objects.all()
    p = Paginator(book_lists,2)
    try:
        book_list = p.page(page_number)
    except EmptyPage:
        book_list = p.page(p.num_pages)
    except PageNotAnInteger:
        book_list = p.page(1)
    return render(request, 'index.html', locals())


def addbook(request):
    if request.method=='GET':
        book_id=request.GET.get('id')
        book=models.Book.objects.filter(id=book_id).first()
        publish=models.Publish.objects.all()
        authors=models.Author.objects.all()
        classify=models.Classify.objects.all()
        return render(request, 'addbook.html', locals())
    else:
        d={}
        d['title']=request.POST.get('title')
        d['price']= price=request.POST.get('price')
        d['publish_id']=request.POST.get('publish_id')
        d['date']=request.POST.get('date')
        d['classify_id']=request.POST.get('classify_id')
        book_obj=models.Book.objects.create(**d)
        authors_id=request.POST.getlist('authors_id')
        authors=models.Author.objects.filter(id__in=authors_id)
        print(authors)
        book_obj.author.add(*authors)
        book_obj.save()
        return redirect('/index/')

def delbook(request):
    book_id=request.GET.get('id')
    models.Book.objects.filter(id=book_id).delete()
    return redirect('/index/')

def editbook(request):
    if request.method == 'GET':
        bookid=request.GET.get('id')
        book_obj=models.Book.objects.filter(id=bookid).first()
        publishs=models.Publish.objects.all()
        publish=book_obj.publish
        classifys=models.Classify.objects.all()
        classify=book_obj.classify
        authors=models.Author.objects.all()
        author_list=[]
        for author in book_obj.author.all():
            author_list.append(author.id)
        return render(request,'editbook.html',locals())
    if request.method == 'POST':
        book_id=request.GET.get('id')
        d = {}
        d['title'] = request.POST.get('title')
        d['price'] = price = request.POST.get('price')
        d['publish_id'] = request.POST.get('publish_id')
        d['date'] = request.POST.get('date')
        d['classify_id'] = request.POST.get('classify_id')
        models.Book.objects.filter(id=book_id).update(** d)
        book_obj =models.Book.objects.filter(id=book_id).first()
        book_obj.author.clear()
        authors_id = request.POST.getlist('authors_id')
        authors = models.Author.objects.filter(id__in=authors_id)
        book_obj.author.add(*authors)
        book_obj.save()
        return redirect('/index/')

def query(request):
    if request.method=='POST':
        title=request.POST.get('book')
        if title:
            books=models.Book.objects.filter(title__icontains=title)
            return render(request,'query.html',locals())
        else:
            return redirect('/index/')


#------------------------------------------单表操作
def menu_author(request):
    page_number = request.GET.get("page")
    book_lists =authors=models.Author.objects.all()
    p = Paginator(book_lists,2)
    try:
        book_list = p.page(page_number)
    except EmptyPage:
        book_list = p.page(p.num_pages)
    except PageNotAnInteger:
        book_list = p.page(1)
    return render(request,'menu_author.html',locals())


def menu_author_add(request):
    name=request.POST.get('name')
    sex=request.POST.get('sex')
    age=request.POST.get('age')
    university=request.POST.get('university')
    models.Author.objects.create(name=name,sex=sex,age=age,university=university)
    return HttpResponse('ok')


def menu_author_edit(request):
    if request.method=='GET':
        id=request.GET.get('id')
        author_obj=models.Author.objects.get(id=id)
        return render(request,'menu_author_edit.html',locals())
    else:
        id=request.GET.get('id')
        name=request.POST.get('name')
        sex=request.POST.get('sex')
        age=request.POST.get('age')
        university=request.POST.get('university')
        models.Author.objects.filter(id=id).update(name=name,sex=sex,age=age,university=university)
        return redirect('/ul/menu/author/')

def menu_author_del(request):
        id=request.GET.get('id')
        models.Author.objects.filter(id=id).delete()
        return redirect('/ul/menu/author/')


#出版社单表
def menu_publish(request):
    page_number = request.GET.get("page")
    book_lists = authors = models.Publish.objects.all()
    p = Paginator(book_lists, 2)
    try:
        book_list = p.page(page_number)
    except EmptyPage:
        book_list = p.page(p.num_pages)
    except PageNotAnInteger:
        book_list = p.page(1)
    return render(request, 'menu_publish.html', locals())

def menu_publish_add(request):
    name=request.POST.get('name')
    addr=request.POST.get('addr')
    models.Publish.objects.create(name=name,addr=addr)
    return HttpResponse('ok')

def menu_publish_edit(request):
    if request.method=='GET':
        id=request.GET.get('id')
        publish=models.Publish.objects.get(id=id)
        return render(request,'menu_publish_edit.html',locals())
    else:
        id=request.GET.get('id')
        name=request.POST.get('name')
        addr=request.POST.get('addr')
        models.Publish.objects.filter(id=id).update(name=name,addr=addr)
        return redirect('/ul/menu/publish/')

def menu_publish_del(request):
    id=request.GET.get('id')
    models.Publish.objects.filter(id=id).delete()
    return redirect('/ul/menu/publish/')



#数据类别 单表
def menu_classify(request):
    page_number = request.GET.get("page")
    book_lists = authors = models.Classify.objects.all()
    p = Paginator(book_lists, 2)
    try:
        book_list = p.page(page_number)
    except EmptyPage:
        book_list = p.page(p.num_pages)
    except PageNotAnInteger:
        book_list = p.page(1)
    return render(request,'menu_classify.html', locals())


def menu_classify_add(request):
    category=request.POST.get("classify")
    models.Classify.objects.create(category=category)
    return HttpResponse('ok')


def menu_classify_edit(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        classify = models.Classify.objects.get(id=id)
        return render(request, 'menu_classify_edit.html', locals())
    else:
        id = request.GET.get('id')
        category = request.POST.get('category')
        models.Classify.objects.filter(id=id).update(category=category)
        return redirect('/ul/menu/classify/')


def menu_classify_del(request):
    id=request.GET.get('id')
    models.Classify.objects.filter(id=id).delete()
    return redirect('/ul/menu/classify/')











def ormadd(request):
    #orm2添加一条记录的方法
    #单表
    #1、表.objects.create（）
    models.Publish.objects.create(name='浙江出版社',addr="浙江.杭州")
    models.Classify.objects.create(category='武侠')
    models.Author.objects.create(name='金庸',sex='男',age=89,university='东吴大学')
    # #2.obj=类（属性=XX） obj.save()
    obj=models.Author(name='吴承恩',age=518,sex='男',university='龙溪学院')
    obj.save()

    # 1对多
    # 1.表.objects.create()
    models.Book.objects.create(title='笑傲江湖',price=200,date=1968,classify_id=6, publish_id=6)
    #2、obj=类（属性=X,外键=obj）obj.save()
    classify_obj=models.Classify.objects.get(category='武侠')
    publish_obj=models.Publish.objects.get(name='河北出版社')
    # #注意以上获取得是和 book对象 向关联的（外键）的对象
    book_obj=models.Book(title='西游记',price=234,date=1556,classify=classify_obj,publish=publish_obj)
    book_obj.save()

    #多对多：如果两表之间存在双向1对N关系，就无法使用外键来描述其关系了；
    # 只能使用多对多的方式，新增第三张表关系描述表；
    book=models.Book.objects.get(title='笑傲江湖')
    author1=models.Author.objects.get(name='金庸')
    author2=models.Author.objects.get(name='张根')
    book.author.add(author1,author2)
    # 书籍和作者是多对多关系，
    # 切记：如果两表之间存在多对多关系，例如书籍相关的所有作者对象集合，作者也关联的所有书籍对象集合
    book=models.Book.objects.get(title='西游记')
    author=models.Author.objects.get(name='吴承恩')
    author2 = models.Author.objects.get(name='张根')
    book.author.add(author,author2)
    #add()   添加
    #clear() 清空
    #remove() 删除某个对象
    return HttpResponse('OK')


def ormquery(request):
    # books=models.Book.objects.all()  #------query_set对象集合 [对象1、对象2、.... ]
    # books=models.Book.objects.filter(id__gt=2,price__lt=100)
    # book=models.Book.objects.get(title__endswith='金') #---------单个对象，没有找到会报错
    # book1 = models.Book.objects.filter(title__endswith='金').first()
    # book2 = models.Book.objects.filter(title__icontains='瓶').last()
    # books=models.Book.objects.values('title','price',        #-------query_set字典集合 [{一条记录},{一条记录} ]
    #                                 'publish__name',
    #                                 'date',
    #                                 'classify__category',  #切记 正向连表:外键字段___对应表字段
    #                                 'author__name',         #反向连表： 小写表名__对应表字段
    #                                 'author__sex',          #区别：正向 外键字段__，反向 小写表名__
    #                                 'author__age',
    #                                 'author__university')
    #
    # books=models.Book.objects.values('title','publish__name').distinct()
    #                                                     #exclude 按条件排除。。。
    #                                                     #distinct()去重,查看数据 是否存在 返回 true 和false
    # a=models.Book.objects.filter(title__icontains='金').exists()
    return HttpResponse('OK')


def queryset(request):
    books=models.Book.objects.all()[:10]  #切片 应用分页
    books = models.Book.objects.all()[::2]
    book= models.Book.objects.all()[6]    #索引
    print(book.title)
    for obj in books:                     #可迭代
        print(obj.title)
    books=models.Book.objects.all()          #惰性计算--->等于一个生成器，不应用books不会执行任何SQL操作
    # query_set缓存机制1次数据库查询结果query_set都会对应一块缓存，再次使用该query_set时，不会发生新的SQL操作；
    #这样减小了频繁操作数据库给数据库带来的压力;
    authors=models.Author.objects.all()
    for author in  authors:
        print(author.name)
    print('-------------------------------------')
    models.Author.objects.filter(id=1).update(name='张某')
    for author in  authors:
        print(author.name)
    #但是有时候取出来的数据量太大会撑爆缓存，可以使用迭代器优雅得解决这个问题；
    models.Publish.objects.all().iterator()
    return HttpResponse('OK')


def relation(request):
    #查询<<我的奋斗>>这本书的作者 name、sex、age、 university
    # author_info=models.Book.objects.filter(title__icontains="我的奋斗").values('author__name',
    #                                                                        'author__sex',
    #                                                                        'author__university'  )
    #反向查询
    author_info=models.Author.objects.filter(book__title__icontains="我的奋斗").values('name',
                                                                                'age',
                                                                                'university')
    # 查询<<我的奋斗>>这本书的作者出版社地址
    # publish=models.Book.objects.filter(title__icontains='我的奋斗').values('publish__name',
    #                                                                         'publish__addr')
    # publish=models.Publish.objects.filter(book__title='我的奋斗').values('addr','name')
    # print(publish)
    # books=models.Publish.objects.filter(name__contains='河北').values('name','book__title')
    # print(books)
    #---------------------------------------------------------
    # #反向连表查询：查询湖南出版社出版过的书
    # #1、通过object的形式反向连表， obj.小写表名_set.all()
    # publish=models.Publish.objects.filter(name__contains='湖南').first()
    # books=publish.book_set.all()
    # for book in  books:
    #     print(book.title)
    # # #反向绑定外键关系
    # authorobj = models.Author.objects.filter(id=1).first()
    # objects = models.Book.objects.all()
    # authorobj.book_set.add(*objects)
    # authorobj.save()
    # #
    # # 2、通过values双下滑线的形式，objs.values("小写表名__字段")
    # #注意对象集合调用values（），正向查询是外键字段__XX,而反向是小写表名__YY看起来比较容易混淆；
    # books=models.Publish.objects.filter(name__contains='湖南').values('name','book__title')
    # authors=models.Book.objects.filter(title__icontains='我的').values('author__name')
    # print(authors)
    # #fifter()也支持__小写表名语法进行连表查询：在publish标查询 出版过《笑傲江湖》的出版社
    # publishs=models.Publish.objects.filter(book__title='笑傲江湖').values('name')
    # print(publishs)
    # #查询谁（哪位作者）出版过的书价格大于200元
    # authors=models.Author.objects.filter(book__price__gt=200).values('name')
    # print(authors)
    # #通过外键字段正向连表查询， 出版自保定的书籍
    # city=models.Book.objects.filter(publish__addr__icontains='保定').values('title')
    # print(city)
    obj=HttpResponse()
    obj.status_code=403
    return obj


def aggregate_annotate(request):
    from django.db.models import Avg,Sum,Max,Min
    #求书籍的平均价
    ret=models.Book.objects.all().aggregate(Avg('price'))
    #{'price__avg': 145.23076923076923}

    #参与西游记著作的作者中最老的一位作者
    ret=models.Book.objects.filter(title__icontains='西游记').values('author__age').aggregate(Max('author__age'))
    #{'author__age__max': 518}

    #查看根哥出过得书中价格最贵一本
    ret=models.Author.objects.filter(name__contains='根').values('book__price').aggregate(Max('book__price'))
    #{'book__price__max': Decimal('234.000')}

    #查看每一位作者出过的书中最贵的一本（按作者名分组 values() 然后annotate 分别取每人出过的书价格最高的）
    ret=models.Book.objects.values('author__name').annotate(Max('price'))
    # < QuerySet[
    # {'author__name': '吴承恩', 'price__max': Decimal('234.000')},
    # {'author__name': '吕不韦','price__max': Decimal('234.000')},
    # {'author__name': '姜子牙', 'price__max': Decimal('123.000')},
    # {'author__name': '亚微',price__max': Decimal('123.000')},
    # {'author__name': '伯夷 ', 'price__max': Decimal('2010.000')},
    # {'author__name': '叔齐','price__max': Decimal('200.000')},
    # {'author__name': '陈涛', 'price__max': Decimal('234.000')},
    # {'author__name': '高路川', price__max': Decimal('234.000')}
    # ] >

    #查看每本书的作者中最老的    按作者姓名分组 分别求出每组中年龄最大的
    ret=models.Book.objects.values('author__name').annotate(Max('author__age'))
    # < QuerySet[
    # {'author__name': '吴承恩', 'author__age__max': 518},
    #  {'author__name': '张X', 'author__age__max': 18},
    #  { 'author__name': '张X杰', 'author__age__max': 56},
    #  {'author__name': '方X伟', 'author__age__max': 26},
    #  {'author__name': '游X兵', 'author__age__max': 35},
    #  {'author__name': '金庸', 'author__age__max': 89},
    # { 'author__name': 'X涛', 'author__age__max': 27},
    # {'author__name': '高XX', 'author__age__max': 26}
    # ] >

    #查看 每个出版社 出版的最便宜的一本书
    ret=models.Book.objects.values('publish__name').annotate(Min('price'))
    # < QuerySet[
    # {'publish__name': '北大出版社','price__min': Decimal('67.000')},
    # {'publish__name': '山西出版社','price__min': Decimal('34.000')},
    # {'publish__name': '河北出版社', 'price__min': Decimal('123.000')},
    # {'publish__name': '浙江出版社', 'price__min': Decimal('2.000')},
    # {'publish__name': '湖北出版社', 'price__min': Decimal('124.000')},
    # {'publish__name': '湖南出版社',price__min': Decimal('15.000')}
    # ] >
    return HttpResponse('ok')

def FandQ(request):
    from django.db.models import F,Q
    # 1、F 可以获取对象中的字段的属性（列），并且对其进行操作；
    # models.Book.objects.all().update(price=F('price')+1)
    # 2、Q多条件组合查询
    #如果 多个查询条件 涉及到逻辑使用 fifter（,隔开）可以表示与，但没法表示或非得关系
    #查询 书名包含作者名的书
    book=models.Book.objects.filter(title__icontains='伟',author__name__contains='伟').values('title')
    #如何让orm 中得 fifter 支持逻辑判断+多条件查询？ Q（）登场
    book=models.Book.objects.filter(Q(title__icontains='伟') & Q(author__name__contains='伟')).values('title')
    book=models.Book.objects.filter(Q(author__name__contains='伟') & ~Q(title__icontains='伟')).values('title')

   #多条件包含组合查询
   #查询作者姓名中包含 方/少/伟/书名包含伟3字 并且出版社地址以山西开头的书
    book=models.Book.objects.filter(
                                    Q(
                                    Q(author__name__contains='方') |
                                    Q(author__name__contains='少') |
                                    Q(title__icontains='伟')|
                                    Q(author__name__contains='伟')
                                    )
                                    &
                                    Q(publish__addr__contains='山西')
                                    ).values('title')

    # 修改方式1
    models.Book.objects.filter(id=1).update(price=3)
    #方式2
    book_obj=models.Book.objects.get(id=1)
    book_obj.price=5
    book_obj.save()
    return HttpResponse('OK')




