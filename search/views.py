from django.shortcuts import render
from app.models import Product
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger,InvalidPage
 
def search_result(request):
    products = None
    query = None
    #検索機能の実装
    if 'q' in request.GET:
        query = request.GET.get('q')
        products = Product.objects.all().filter(Q(name__contains=query)|Q(description__contains=query),available=True)
    liked_list = []
    user=request.user
    if user.is_authenticated:
        for product in products:
            liked = product.likeforproduct_set.filter(user=request.user)
            if liked.exists():
                liked_list.append(product.id)
    #ページネーションの実装
    count = 9
    paginator = Paginator(products, count)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    csrf_token = request.GET.get('csrfmiddlewaretoken')
    return render(request, 'search.html', {'query': query, 'products': products,'csrf_token':csrf_token,'count':count,'liked_list': liked_list})