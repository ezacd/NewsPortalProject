from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.db.models import Sum

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from NewsPortal.settings import *


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_posts_author = Post.objects.filter(author_id=self.pk).aggregate(rating=Sum('rating'))['rating']
        rating_comments_author = \
            Comment.objects.filter(user_id=self.user).aggregate(comment_rating=Sum('comment_rating'))['comment_rating']
        rating_comments_posts = \
            Comment.objects.filter(post__author__user=self.user).aggregate(comment_rating=Sum('comment_rating'))[
                'comment_rating']
        self.rating = rating_posts_author * 3 + rating_comments_author + rating_comments_posts
        self.save()

    def __str__(self):
        return str(self.user)


class Category(models.Model):
    tech = 'TE'
    politics = 'PO'
    sport = 'SP'
    culture = 'CU'
    education = 'ED'
    CATEGORIES = [
        (tech, 'Техника'),
        (politics, 'Политика'),
        (sport, 'Спорт'),
        (culture, 'Культура'),
        (education, 'Образование')
    ]

    name = models.CharField(max_length=2, choices=CATEGORIES, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name


class Post(models.Model):
    article = 'AR'
    news = 'NE'
    POST_TYPES = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES)
    data = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.header}: {self.text}...'

    def like(self):
        self.rating += 1
        self.save()
        return self.rating

    def dislike(self):
        self.rating -= 1
        self.save()
        return self.rating

    def preview(self):
        return f'{self.text[:124]}...'

    def get_absolute_url(self):
        return reverse('default', args='')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()
        return self.comment_rating

    def dislike(self):
        self.comment_rating -= 1
        self.save()
        return self.comment_rating


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)

        send_mail(
            subject=f'{user.username} вы зарегистрированы',
            message='',
            from_email=DEFAULT_FROM_EMAIL,
            html_message=render_to_string('register_user.html', {'user': user.username}),
            recipient_list=[user.email, ],

        )
        return user
