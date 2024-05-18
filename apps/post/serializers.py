from rest_framework import serializers

from .models import Post, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["id", "image", "order"]


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    total_views = serializers.SerializerMethodField(read_only=True)
    total_likes = serializers.SerializerMethodField(read_only=True)
    author_name = serializers.SerializerMethodField(read_only=True)
    author_city = serializers.SerializerMethodField(read_only=True)
    upload_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=True),
        write_only=True,
    )

    def get_total_views(self, instance: Post) -> int:
        return instance.total_views

    def get_total_likes(self, instance: Post) -> int:
        return instance.total_likes

    def get_author_name(self, instance: Post) -> str:
        return instance.author_name

    def get_author_city(self, instance: Post) -> str:
        return instance.author_city

    def create(self, validated_data):
        images = validated_data.pop("upload_images")
        post = Post.objects.create(**validated_data)
        order = 0
        for image in images:
            PostImage.objects.create(post=post, image=image, order=order)
            order += 1
        return post

    class Meta:
        model = Post
        fields = [
            "id",
            "headline",
            "content",
            "link",
            "author_name",
            "author_city",
            "total_views",
            "total_likes",
            "images",
            "created_at",
            "upload_images",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "view_count": {"read_only": True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not self.context.get("detail", True):
            data.pop("total_views")
            data.pop("link")
            data.pop("total_likes")
        return data
