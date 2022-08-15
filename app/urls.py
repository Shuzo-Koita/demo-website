from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import SignupView, ContactView,LoginView,ContactCompleteView
from . import views 

app_name='app'

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('whole/', views.WholeCake.as_view()),
    path('roll/', views.RollCake.as_view()),
    path('cup/', views.CupCake.as_view()),
    path('cookie/', views.Cookie.as_view()),
    path('favorite/', views.favorite),
    path('contact/', ContactView.as_view(),name = "contact"),
    path('contact/complete/', ContactCompleteView.as_view()),
    path('signup/', SignupView.as_view()),
    path('signup/done', views.SignupDone.as_view(), name='signup_done'),
    path('signup/complete/<token>/', views.SignupComplete.as_view(), name='signup_complete'),
    path('topics/', views.Topics.as_view(), name="topics"), 
    path('detail/<pk>/', views.Detail.as_view(), name="Detail"),
    path('login/', LoginView.as_view(), name='login'),
    path('account/', views.AccountView.as_view()),
    path('account/complete/', views.AccountCompleteView.as_view()),
    path('like', views.LikeView, name='like'),
    # path('logout/', views.Logout.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)