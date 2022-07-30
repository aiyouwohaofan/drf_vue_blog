from .models import Article, Category, Label, Avatar
from .permissions import IsAdminUserOrReadOnly
from rest_framework import viewsets, filters
from article.serializers import ArticleSerializer, CategorySerializer, CategoryDetailSerializer, AvatarSerializer
from article.serializers import LabelSerializer, ArticleCategoryDetailSerializer, ArticleDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend


class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['author__username', 'title']
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleCategoryDetailSerializer
        else:
            return ArticleSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        else:
            return ArticleDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None
