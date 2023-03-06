from django.contrib import admin
from django.urls import path, include

# Это основной файл urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('News.urls')),
    path('article/', include('News.article_urls')),
]
