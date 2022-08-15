from itertools import product
from multiprocessing import context
from re import T
from unicodedata import category
from django.views.generic import TemplateView, ListView, DetailView
from .models import Post, Product, Profile, LikeForProduct
from django.shortcuts import get_object_or_404,render,redirect
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.conf import settings
from django.http import Http404, HttpResponseBadRequest
from django.contrib.auth.forms import (
    AuthenticationForm
)
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage,InvalidPage

User = get_user_model()

# def set_submit_token(request):
#     submit_token = str(uuid.uuid4())
#     request.session['submit_token'] = submit_token
#     return submit_token

# def exists_submit_token(request):
#     token_in_request = request.POST.get('submit_token')
#     token_in_session = request.session.POP('submit_token', '')

#     if not token_in_request:
#         return False
#     if not token_in_session:
#         return False

#     return token_in_request == token_in_session

class ContactView(TemplateView):
    template_name = "contact.html"
    def get_context_data(self):
        ctxt = super().get_context_data()
        ctxt["subtitle"] = " | お問い合わせフォーム"
        return ctxt
    def post(self, request, *args, **kwargs):
        subject = request.POST["category"]
        name = request.POST["name"]
        tel = request.POST["tel"]
        email = request.POST["email"]
        orderNumber = request.POST["orderNumber"]
        detail = request.POST["detail"]
        message = "名前：" + name + "様\n電話番号：" + tel + "\nメールアドレス：" \
            + email + "\n注文番号：" + orderNumber + "\n内容：" + detail
        from_email = "jesus.christ.is.the.lord19860804@gmail.com"
        to = ["jesus.christ.is.the.lord19860804@gmail.com"]
        send_mail(subject, message, from_email, to)
        return redirect("complete/", {})

class ContactCompleteView(TemplateView):
    template_name = "contact_complete.html"
    def get_context_data(self):
        ctxt = super().get_context_data()
        ctxt["subtitle"] = " | お問い合わせ完了"
        return ctxt

# class WholeCake(ListView):
#     template_name = "product_list.html"
#     queryset = Product.objects.filter(category=2,available=True)
#     ordering = '-updated'
#     paginate_by = 9
#     def get_context_data(self):
#         ctxt = super().get_context_data()
#         ctxt["subtitle"] = " | ホールケーキ"
#         ctxt["headline"] = "ホールケーキ"
#         return ctxt

def WholeCake(request):
    products = Product.objects.filter(category=2,available=True)
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
    # csrf_token = request.GET.get('csrfmiddlewaretoken')
    context = {
        'liked_list': liked_list,
        'subtitle': ' | ホールケーキ',
        'headline': 'ホールケーキ',
        'products': products,
        # 'csrf_token':csrf_token,
        'count':count,
    }
    return render(request, 'product_list.html', context)

def LikeView(request):
    user = request.user
    if request.method =="POST" and user.is_authenticated:
        product = get_object_or_404(Product, pk=request.POST.get('product_id'))
        liked = False
        like = LikeForProduct.objects.filter(product=product, user=user)
        if like.exists():
            like.delete()
        else:
            like.create(product=product, user=user)
            liked = True
    
        context={
            'product_id': product.id,
            'liked': liked,
            'count': product.likeforproduct_set.count(),
        }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(context)

class Index(ListView):
    template_name = "index.html"
    queryset = Post.objects.filter(category=1)
    ordering = '-updated'
    def get_context_data(self):
        ctxt = super().get_context_data()
        ctxt["subtitle"] = ""
        return ctxt

class Topics(ListView):
    template_name = "topics_list.html"
    queryset = Post.objects.filter(category=1)
    ordering = '-updated'
    paginate_by = 5
    def get_context_data(self):
        ctxt = super().get_context_data()
        ctxt["subtitle"] = " | トピックス"
        return ctxt

class Detail(DetailView):
    model = Product

class SignupView(TemplateView):
    template_name = "signup.html"
    def get_context_data(self):
        ctxt = super().get_context_data()
        ctxt["subtitle"] = " | 新規会員登録"
        return ctxt

    def post(self, request, *args, **kwargs):
        username2 = request.POST['email']
        try:
            User.objects.get(username = username2)
            return render(request, "signup.html", {"error":"メールアドレスがすでに登録されています！"}) 
        except:
            display_name = request.POST['name']
            furigana = request.POST['furigana']
            postal = request.POST['postal']
            pref_id = request.POST['pref_id']
            address1 = request.POST['address1']
            address2 = request.POST['address2']
            tel = request.POST['tel']
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.create_user(username2, email, password)
            user.profile.display_name = display_name
            user.profile.furigana = furigana
            user.profile.postal = postal
            user.profile.pref_id = pref_id
            user.profile.address1 = address1
            user.profile.address2 = address2
            user.profile.tel = tel
            user.profile.email = email
            user.is_active = False
            user.save()

            # アクティベーションURLの送付
            current_site = get_current_site(self.request)
            domain = current_site.domain
            context = {
                'protocol': self.request.scheme,
                'domain': domain,
                'token': dumps(user.pk),
                'display_name': display_name,
            }
            subject = "西洋洋菓子店 － 会員登録"
            message = render_to_string('app/mail_template/signup/message.txt', context)
            from_email = "jesus.christ.is.the.lord19860804@gmail.com"
            to = [email]
            send_mail(subject, message, from_email, to)
            return render(request, 'signup_done.html')

class SignupDone(TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'signup_done.html'


class SignupComplete(TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'signup_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)
        return HttpResponseBadRequest()

# class LoginForm(AuthenticationForm):
#     """ログインフォーム"""

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
#             field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる

class Login(LoginView):
    """ログインページ"""
    template_name = 'login.html'


# class Logout(LogoutView):
#     """ログアウトページ"""
#     template_name = 'index.html'

class AccountView(TemplateView):
    template_name = "account.html"
    def get_context_data(self):
        ctxt = super().get_context_data()
        ctxt["subtitle"] = " | アカウント情報"
        return ctxt

    def post(self, request, *args, **kwargs):
        username = request.POST['email']
        display_name = request.POST['name']
        furigana = request.POST['furigana']
        postal = request.POST['postal']
        pref_id = request.POST['pref_id']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        tel = request.POST['tel']
        user = User.objects.get(username=username)
        user.profile.display_name = display_name
        user.profile.furigana = furigana
        user.profile.postal = postal
        user.profile.pref_id = pref_id
        user.profile.address1 = address1
        user.profile.address2 = address2
        user.profile.tel = tel
        user.save()
        return redirect('complete/',{})

class AccountCompleteView(TemplateView):
    template_name = "account_complete.html"
    def get_context_data(self):
        ctxt = super().get_context_data()
        ctxt["subtitle"] = " | アカウント情報更新完了"
        return ctxt

# class RollCake(ListView):
#     template_name = "product_list.html"
#     queryset = Product.objects.filter(category=3,available=True)
#     ordering = '-updated'
#     paginate_by = 9
#     def get_context_data(self):
#         ctxt = super().get_context_data()
#         ctxt["subtitle"] = " | ロールケーキ"
#         ctxt["headline"] = "ロールケーキ"
#         return ctxt

def RollCake(request):
    products = Product.objects.filter(category=3,available=True)
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
    # csrf_token = request.GET.get('csrfmiddlewaretoken')
    context = {
        'liked_list': liked_list,
        'subtitle': ' | ロールケーキ',
        'headline': 'ロールケーキ',
        'products': products,
        # 'csrf_token':csrf_token,
        'count':count,
    }
    return render(request, 'product_list.html', context)

# class CupCake(ListView):
#     template_name = "product_list.html"
#     queryset = Product.objects.filter(category=4,available=True)
#     ordering = '-updated'
#     paginate_by = 9
#     def get_context_data(self):
#         ctxt = super().get_context_data()
#         ctxt["subtitle"] = " | マフィン"
#         ctxt["headline"] = "マフィン"
#         return ctxt

def CupCake(request):
    products = Product.objects.filter(category=4,available=True)
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
    # csrf_token = request.GET.get('csrfmiddlewaretoken')
    context = {
        'liked_list': liked_list,
        'subtitle': ' | マフィン',
        'headline': 'マフィン',
        'products': products,
        # 'csrf_token':csrf_token,
        'count':count,
    }
    return render(request, 'product_list.html', context)

# class Cookie(ListView):
#     template_name = "product_list.html"
#     queryset = Product.objects.filter(category=5,available=True)
#     ordering = '-updated'
#     paginate_by = 9
#     def get_context_data(self):
#         ctxt = super().get_context_data()
#         ctxt["subtitle"] = " | クッキー"
#         ctxt["headline"] = "クッキー"
#         return ctxt

def Cookie(request):
    products = Product.objects.filter(category=5,available=True)
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
    # csrf_token = request.GET.get('csrfmiddlewaretoken')
    context = {
        'liked_list': liked_list,
        'subtitle': ' | クッキー',
        'headline': 'クッキー',
        'products': products,
        # 'csrf_token':csrf_token,
        'count':count,
    }
    return render(request, 'product_list.html', context)

def favorite(request):
    products = Product.objects.all()
    liked_list = []
    user=request.user
    if user.is_authenticated:
        for product in products:
            liked = product.likeforproduct_set.filter(user=request.user)
            if liked.exists():
                liked_list.append(product.id)
    products = Product.objects.filter(id__in= liked_list)
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
    # csrf_token = request.GET.get('csrfmiddlewaretoken')
    context = {
        'liked_list': liked_list,
        'subtitle': ' | お気に入り',
        'headline': 'お気に入り',
        'products': products,
        # 'csrf_token':csrf_token,
        'count':count,
    }
    return render(request, 'product_list.html', context)