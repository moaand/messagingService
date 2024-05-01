from rest_framework import serializers
from .models import Message, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name', 'date_accessed']

class MessageSerializer(serializers.ModelSerializer):

    sender = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    receiver = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = Message
        fields = ['id','content', 'sender','receiver', 'created_at']