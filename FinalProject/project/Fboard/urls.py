from django.urls import path, include
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', cache_page(60*10)(PostDetailView.as_view()), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('personal/', PersonalAreaView.as_view(), name='personal_area'),
    path('post/<int:pk>/reply/', reply, name='reply'),
    path('post/<int:pk>/replied/', replied, name='replied'),
    path('personal/<int:pk>/', ReplyDetailView.as_view(), name='reply_detail'),
    path('personal/<int:pk>/delete/', ReplyDeleteView.as_view(), name='reply_delete'),
    path('personal/<int:pk>/approve/', reply_approve, name='reply_approve'),
    path('personal/by_post/<int:post_id>/', SortedByPostView.as_view(), name='sorted_by_post'),
    path('subscribe/', subscribe, name='subscribe'),
    path('unsubscribe/', unsubscribe, name='unsubscribe'),
]


