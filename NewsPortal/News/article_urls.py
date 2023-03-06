from django.urls import path

from .views import PostList, PostDetail, SearchList, ArticleCreate, ArticleUpdate, ArticleDelete

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', SearchList.as_view(), name='post_list'),
    path('create/', ArticleCreate.as_view()),
    path('<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]