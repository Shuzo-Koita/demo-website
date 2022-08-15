from .models import Product,LikeForProduct

def like(request):
    products = Product.objects.all()
    liked_list = []
    user=request.user
    if user.is_authenticated:
        for product in products:
            liked = product.likeforproduct_set.filter(user=request.user)
            if liked.exists():
                liked_list.append(product.id)
    return dict(liked_list = liked_list)