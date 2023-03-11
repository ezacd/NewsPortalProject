from django_filters import FilterSet, DateFilter
from .models import Post
from django.forms import DateInput


class PostFilter(FilterSet):
    data = DateFilter(field_name='data', widget=DateInput(attrs={'type': 'date'}), label='Поиск по дате', lookup_expr='date__gte')

    class Meta:
        model = Post
        fields = {
            'header': ['icontains'],
            'author_id__user_id__username': ['icontains'],
        }