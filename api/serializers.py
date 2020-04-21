from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
	appky = serializers.JSONField()
	class Meta:
		model = Post
		fields = ('appky',)