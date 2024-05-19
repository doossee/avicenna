from rest_framework import serializers

from .models import User, DiseaseCategory, DiseasePost, DiseasePostAttachment, Comment

from src.management.serializers import UserSerializer


class DiseaseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseCategory
        fields = '__all__'


class DiseasePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseasePost
        fields = '__all__'


class DiseasePostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseasePostAttachment
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


# class DiseaseCategorySerializer(serializers.ModelSerializer):

#     """Disease category serializer"""
    
#     class Meta:
#         model = DiseaseCategory
#         fieldss = '__all__'

# class DiseasePostAttachmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DiseasePostAttachment
#         fieldss = '__all__'
        

# class DiseasePostSerializer(serializers.ModelSerializer):
#     sender = UserSerializer(read_only=True)
#     categories = DiseaseCategorySerializer(read_only=True)
#     attachments = DiseasePostAttachmentSerializer(many=True, read_only=True)
#     views = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)

#     class Meta:
#         model = DiseasePost
#         fieldss = '__all__'
#         read_only_fields = ['created_at', 'updated_at']

# class CommentSerializer(serializers.ModelSerializer):
#     sender = UserSerializer(read_only=True)
#     post = DiseasePostSerializer(read_only=True)
#     parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), allow_null=True, required=False)
#     likes = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
#     dislikes = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)

#     class Meta:
#         model = Comment
#         fields = ['id', 'sender', 'post', 'parent', 'content', 'likes', 'dislikes', 'created_at', 'updated_at']
#         read_only_fields = ['created_at', 'updated_at']
