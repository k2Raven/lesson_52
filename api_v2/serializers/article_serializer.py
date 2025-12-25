from rest_framework import serializers

from webapp.models import Tag, Article


class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50, required=True)
    content = serializers.CharField(required=True)
    author_id = serializers.IntegerField(required=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        return super().validate(attrs)

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError('Title must be at least 5 characters long.')
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        article = Article.objects.create(**validated_data)
        article.tags.set(tags)
        return article

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.tags.set(tags)
        return instance

