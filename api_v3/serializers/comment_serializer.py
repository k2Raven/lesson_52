from rest_framework import serializers

from webapp.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


