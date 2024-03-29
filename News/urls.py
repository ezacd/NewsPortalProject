from django.urls import path

from .views import PostList, PostDetail, SearchList, NewsCreate, \
    NewsUpdate, NewsDelete, upgrade_me, CategoryListView, subscribe

urlpatterns = [
    path('', PostList.as_view(), name='default'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', SearchList.as_view(), name='post_list'),
    path('create/', NewsCreate.as_view()),
    path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe')
]
