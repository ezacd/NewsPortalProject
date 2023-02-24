from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


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
