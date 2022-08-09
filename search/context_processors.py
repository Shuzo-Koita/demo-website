from app.models import Product
from django.db.models import Q

def search_counter(request):
    search_count = 0
    subtitle = ""
    if 'q' in request.GET:
        query = request.GET.get('q')
        search_count = Product.objects.all().filter(Q(name__contains=query) | Q(description__contains=query),available=True).count()
        subtitle = " | 検索結果"
    return dict(search_count = search_count, subtitle = subtitle)