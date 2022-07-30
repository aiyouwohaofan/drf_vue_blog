from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from markdown import Markdown


class Category(models.Model):
    title = models.CharField(max_length=128, unique=True)
    created = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Label(models.Model):
    label_name = models.CharField(max_length=32, unique=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.label_name


class Avatar(models.Model):
    content = models.ImageField(upload_to='avatar/%Y%m%d')


class Article(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    created = models.DateTimeField(default=datetime.now)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='articles')
    labels = models.ManyToManyField(Label, blank=True, related_name='articles')
    avatar = models.ForeignKey(Avatar, null=True, blank=True, on_delete=models.SET_NULL, related_name='article')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_md(self):
        md = Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        md_body = md.convert(self.content)
        return md_body, md.toc
