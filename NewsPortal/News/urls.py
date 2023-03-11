from django.urls import path

from .views import PostList, PostDetail, SearchList, NewsCreate, NewsUpdate, NewsDelete, upgrade_me

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', SearchList.as_view(), name='post_list'),
    path('create/', NewsCreate.as_view()),
    path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
]
