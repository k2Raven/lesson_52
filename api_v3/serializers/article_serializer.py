from rest_framework import serializers

from webapp.models import Article, Tag
from api_v3.serializers import TagSerializer


class ArticleSerializer(serializers.ModelSerializer):
    # tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), write_only=True)
    # tags_read = TagSerializer(many=True, read_only=True, source='tags')

    class Meta:
        model = Article
        # fields = '__all__'
        fields = ['id', 'title', 'content', 'author', 'tags', 'created_at', 'updated_at',
                  # 'tags_read'
                  ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tags'] = TagSerializer(instance.tags.all(), many=True).data
        return data


    def validate(self, attrs):
        return super().validate(attrs)

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError('Title must be at least 5 characters long.')
        return value

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title']