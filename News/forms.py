from django import forms
from .models import Post, Author


class PostForm(forms.ModelForm):
    header = forms.CharField(min_length=5)
    author = Author.objects.all().values('user_id__username')

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'header',
            'text',
        ]

    def clean(self):
        clean_data = super().clean()
        header = clean_data.get('header')
        text = clean_data.get('text')
        if header == text:
            raise ValueError('Описание не должно быть идентично названию')
        return clean_data