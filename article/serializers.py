from rest_framework import serializers
from .models import Article, Category, Label, Avatar
from user_info.serializers import UserDescSerializer
from comment.serializers import CommentSerializer


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created']


class LabelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'


class AvatarSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='avatar-detail')

    class Meta:
        model = Avatar
        fields = '__all__'


class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = UserDescSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    labels = serializers.SlugRelatedField(
        queryset=Label.objects.all(),
        many=True,
        required=False,
        slug_field='label_name'
    )
    avatar = AvatarSerializer(read_only=True)
    avatar_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    default_error_messages = {
        'incorrect_avatar_id': 'Avatar with id {value} not exists.',
        'incorrect_category_id': 'Category with id {value} not exists.',
        'default': 'No more message here..',
    }

    def check_obj_exists_or_fail(self, model, value, message='default'):
        if not self.default_error_messages.get(message, None):
            message = 'default'
        if not model.objects.filter(id=value).exists() and value is not None:
            self.fail(message, value=value)

    def validate_avatar_id(self, value):
        self.check_obj_exists_or_fail(model=Avatar, value=value, message='incorrect_avatar_id')
        return value

    def validate_category_id(self, value):
        self.check_obj_exists_or_fail(model=Category, value=value, message='incorrect_category_id')
        return value

    def to_internal_value(self, data):
        labels_data = data.get('labels')
        if isinstance(labels_data, list):
            for label_name in labels_data:
                if not Label.objects.filter(label_name=label_name).exists():
                    Label.objects.create(label_name=label_name)
        return super().to_internal_value(data)


class ArticleSerializer(ArticleBaseSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {'content': {'write_only': True}}


class ArticleDetailSerializer(ArticleBaseSerializer):
    content_html = serializers.SerializerMethodField()
    toc_html = serializers.SerializerMethodField()
    id = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    def get_content_html(self, obj):
        return obj.get_md()[0]

    def get_toc_html(self, obj):
        return obj.get_md()[1]

    class Meta:
        model = Article
        fields = '__all__'


class ArticleCategoryDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='article-detail')

    class Meta:
        model = Article
        fields = ['url', 'title']


class CategoryDetailSerializer(serializers.ModelSerializer):
    articles = ArticleCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'created', 'articles']

