from rest_framework import serializers

from webapp.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # fields = '__all__'
        fields = ['id', 'title', 'content', 'author', 'tags', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        return super().validate(attrs)

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError('Title must be at least 5 characters long.')
        return value

