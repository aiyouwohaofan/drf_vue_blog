from django.contrib import admin
from article.models import Article, Category, Label, Avatar


admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Label)
admin.site.register(Avatar)
